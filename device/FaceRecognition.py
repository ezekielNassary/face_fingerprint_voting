from imutils import paths
import face_recognition
import pickle
import cv2
import os
from utils.utils import get_logger
from dataclasses import dataclass
import imutils
from vidgear.gears import VideoGear, CamGear

options = {"THREADED_QUEUE_MODE": True}

# stream = CamGear(source=0, backend=cv2.CAP_DSHOW).start()

@dataclass
class FaceRecognition:
    logger = get_logger(name=__name__)
    dataset: str = None
    encodings: str = None
    detection_method: str = "hog"
    cascade: str = "models/haarcascade_frontalface_default.xml"
    break_loop: bool = True
    stream: VideoGear = VideoGear(
        source=0, logging=True, **options,
    ).start()

    def faces_encoding(self) -> None:
        image_paths = list(paths.list_images(self.dataset))
        known_encodings = []
        known_names = []

        for (i, image_path) in enumerate(image_paths):
            self.logger.info(f"Processing image {i+1}/{len(image_paths)}")
            name = image_path.split(os.path.sep)[-2]

            image = cv2.imread(image_path)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            boxes = face_recognition.face_locations(rgb, model=self.detection_method)
            encodings = face_recognition.face_encodings(rgb, boxes)

            for encoding in encodings:
                known_encodings.append(encoding)
                known_names.append(name)

        self.logger.info("Serializing encodings...")
        data = {"encodings": known_encodings, "names": known_names}
        f = open(self.encodings, "wb")
        f.write(pickle.dumps(data))
        f.close()

    def faces_detection(self) -> None:
        data = pickle.loads(open(self.encodings, "rb").read())
        detector = cv2.CascadeClassifier(self.cascade)

        while True:
            frame = self.stream.read()
            frame = imutils.resize(frame, width=500)

            if frame is None:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            rects = detector.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE,
            )

            boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

            encodings = face_recognition.face_encodings(rgb, boxes)
            names = []
            for encodings in encodings:
                matches = face_recognition.compare_faces(data["encodings"], encodings)
                name = "Unknown"

                if True in matches:
                    matched_ids = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    for i in matched_ids:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    name = max(counts, key=counts.get)
                names.append(name)

            for ((top, right, bottom, left), name) in zip(boxes, names):
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(
                    frame,
                    name,
                    (left, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (0, 255, 0),
                    2,
                )
                self.logger.info("{}".format(name))

            cv2.imshow("Face Recognition", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break
        self.close()

    def close(self) -> None:
        self.stream.stop()
        cv2.destroyAllWindows()
