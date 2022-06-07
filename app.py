from cProfile import run
from importlib import reload
from cv2 import log
from starlette.applications import Starlette
from starlette.responses import JSONResponse
import uvicorn
import serial
from starlette.websockets import WebSocket, WebSocketState
from starlette.responses import FileResponse 
from starlette.staticfiles import StaticFiles
import os, sys
from typing import List
import asyncio
from threading import Thread
import subprocess
import time
import board
import random
#import busio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint
from cv2 import cv2
import os
import time


led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT
import websockets


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from utils.utils import get_logger, get_serial_ports


app = Starlette(debug=True)
logger =get_logger(name=__name__)
ports = get_serial_ports()

script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir, "static/")
app.mount("/static", StaticFiles(directory=st_abs_file_path, html=True), name="static")


clients = set()
import serial
uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

@app.route("/")
async  def index(request):
    return FileResponse(st_abs_file_path + "index.html")



@app.websocket_route("/ws")
async def websocket_endpoint(websocket: WebSocket):
    
    await websocket.accept()
    try:
        while True:
            is_running = True
            # await websocket.send_json({"message": "ping"})
            print("----------------")
            if finger.read_templates() != adafruit_fingerprint.OK:
                raise RuntimeError("Failed to read templates")
            print("Fingerprint templates:", finger.templates)
            print("e) enroll print")
            print("f) find print")
            print("d) delete print")
            print("----------------")
            c = await websocket.receive_text()

            if c == "e":
                await enroll_finger(get_num(),websocket)
            if c == "f":
                if await get_fingerprint(websocket):
                    print("Detected #", finger.finger_id, "with confidence", finger.confidence)
                    await websocket.send_json({"command": "Success"})
                    await websocket.send_json({"id": finger.finger_id})
                else:
                    print("Finger not found")
                    await websocket.send_json({"command": "Finger not found"})
            if c == "d":
                if finger.delete_model(get_num()) == adafruit_fingerprint.OK:
                    print("Deleted!")
                else:
                    print("Failed to delete")
            if c == "t":
                await createDataset(websocket)
                exit()
           
    except Exception as e:
        logger.error(f"Error message f{e}", exc_info=True)
        # await websocket.close()
async def createDataset(websocket):
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
    
    
async def get_fingerprint(websocket):
    await websocket.send_json({"command": "Place finger on sensor"})
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    await websocket.send_json({"command": "Searching....."})
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True
# pylint: disable=too-many-branches
async def get_fingerprint_detail(websocket):
    print("Getting image...", end="", flush=True)
    i = finger.get_image()
    if i == adafruit_fingerprint.OK:
        print("Image taken")
    else:
        if i == adafruit_fingerprint.NOFINGER:
            print("No finger detected")
        elif i == adafruit_fingerprint.IMAGEFAIL:
            print("Imaging error")
        else:
            print("Other error")
        return False

    print("Templating...", end="", flush=True)
    i = finger.image_2_tz(1)
    if i == adafruit_fingerprint.OK:
        print("Templated")
    else:
        if i == adafruit_fingerprint.IMAGEMESS:
            print("Image too messy")
        elif i == adafruit_fingerprint.FEATUREFAIL:
            print("Could not identify features")
        elif i == adafruit_fingerprint.INVALIDIMAGE:
            print("Image invalid")
        else:
            print("Other error")
        return False

    print("Searching...", end="", flush=True)
    i = finger.finger_fast_search()
    # pylint: disable=no-else-return
    # This block needs to be refactored when it can be tested.
    if i == adafruit_fingerprint.OK:
        await websocket.send_json({"command": "Success"})
        print("Found fingerprint!")
               
        return True
    else:
        if i == adafruit_fingerprint.NOTFOUND:
            print("No match found")
            await websocket.send_json({"command": "No match found....."})
        else:
            print("Other error")
        return False
    

# pylint: disable=too-many-statements
async def enroll_finger(location,websocket: WebSocket):
    """Take a 2 finger images and template it, then store in 'location'"""
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Place finger on sensor...", end="", flush=True)
            websocket.send_json({"command": "Place finger on sensor"})
        else:
            print("Place same finger again...", end="", flush=True)
            await websocket.send_json({"command": "Place same finger again"})

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                
                break
            if i == adafruit_fingerprint.NOFINGER:
                await websocket.send_json({"command": "Place Your Finger"})
                print(".", end="", flush=True)
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False
            else:
                print("Other error")
                return False

        print("Templating...", end="", flush=True)
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
            else:
                print("Other error")
            return False

        if fingerimg == 1:
            print("Remove finger")
            await websocket.send_json({"command": "Remove your finger"})
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Creating model...", end="", flush=True)
    await websocket.send_json({"command": "Creating model..."})
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("Created")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("Prints did not match")
            await websocket.send_json({"command": "Prints did not match"})
        else:
            print("Other error")
        return False

    print("Storing model #%d..." % location, end="", flush=True)
    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        print("Stored")
        await websocket.send_json({"command": "Success"})
        await websocket.send_json({"id": location})
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
        elif i == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
        else:
            print("Other error")
        return False

    return True
##################################################



def get_num():
    """Use input() to get a valid number from 1 to 127. Retry till success!"""
    i = 0
    while (i > 127) or (i < 1):
        try:
            #i = int(input("Enter ID # from 1-127: "))
            i=random.randint(0, 128) 
        except ValueError:
            pass
    return i




if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=5555, reload=True)