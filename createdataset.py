from cv2 import cv2
import os
import time

cam_port = 0

#get current directory
current_directory=os.getcwd()

#join to dataset director
new_directory=os.path.join(current_directory, "Dataset")

#change dir to dataset
os.chdir(new_directory)

#input dir name
name = input('Enter voter name: ')

#create voters dir
os.mkdir(name)

#get voter dir
voter_dir=os.getcwd()

#join to dataset director
voter_dir=os.path.join(new_directory, name)

#change dir to voter dir
os.chdir(voter_dir)

#change to voter dir
os.chdir(voter_dir)

for x in range(5):
    #capture image
    cam = cv2.VideoCapture(cam_port)

    #save image
    time.sleep(4)
    result, image = cam.read()
    if result:
        cv2.imshow(name+""+str(x), image)
        cv2.imwrite(name+""+str(x)+".png", image)
        #cv2.waitKey(0)
        #destroyWindow(name)
    else:
        print("No image detected. Please! try again")
    os.listdir()