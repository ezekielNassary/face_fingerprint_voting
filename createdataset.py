from cv2 import cv2
import os
import time

cam_port = 0

#get current directory
current_directory=os.getcwd()

#join to dataset director
new_directory=os.path.join(current_directory, "datasets")

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
time.sleep(10)
for x in range(10):
    #capture image
    cam = cv2.VideoCapture(cam_port)

    #save image
    
    result, image = cam.read()
    if result:
        cv2.imshow(name+""+str(x), image)
        cv2.imwrite(name+""+str(x)+".png", image)
        
        cv2.destroyWindow(name)
        time.sleep(10)
    else:
        print("No image detected. Please! try again")
    os.listdir()