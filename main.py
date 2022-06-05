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
#import busio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

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


@app.route("/")
async  def index(request):
    return FileResponse(st_abs_file_path + "index.html")

uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

@app.websocket_route("/ws")
async def websocket_endpoint(websocket: WebSocket):
    
    await websocket.accept()
    try:
        while True:
            is_running = True
            # await websocket.send_json({"message": "ping"})
            # data = serial_port.readline()
            # data = data.decode()
            # if data != '':
            #     logger.info("Received Data from Serial Port: {}".format(data))
            #     serial_port.flushInput()

            async def read_serial():
                while is_running:
                    print("----------------")
                    if finger.read_templates() != adafruit_fingerprint.OK:
                        raise RuntimeError("Failed to read templates")
                    print("Fingerprint templates:", finger.templates)
                    print("e) enroll print")
                    print("f) find print")
                    print("d) delete print")
                    print("----------------")

                    
            
            message = await websocket.receive_text()
            if message == 'R':
                logger.info(f"Start Training new dataset")
                subprocess.Popen(["python", "fingerprintAdafruit.py"])
            else:
                logger.info(f"Received message from Socket {message}", exc_info=True)
                
                if message == 'train':
                    logger.info(f"Start Training new dataset")
                    subprocess.Popen(["python", "training.py"])
            

    except Exception as e:
        logger.error(f"Error message f{e}", exc_info=True)
        # await websocket.close()


if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=5555, reload=True)
