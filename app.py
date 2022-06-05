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

import websockets


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from utils.utils import get_logger, get_serial_ports


app = Starlette(debug=True)
logger =get_logger(name=__name__)
ports = get_serial_ports()

script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir, "static/")
# app.mount("/static", StaticFiles(directory=st_abs_file_path, html=True), name="static")


clients = set()


@app.route("/")
async  def index(request):
    return FileResponse(st_abs_file_path + "index.html")

ports = get_serial_ports()

_port = None
serial_port = None
for port, desc, hwid in sorted(ports):
    logger.info("{}: {} [{}]".format(port, desc, hwid))
    if "USB-Serial" in desc:
        _port = port
        break



serial_port = serial.Serial(_port, baudrate=9600, timeout=0)


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

                    try:
                        if serial_port.inWaiting() > 0:
                            data = serial_port.readline()
                            data = data.decode()
                            await websocket.send_text(data)
                            logger.info("Received Data from Serial Port: {}".format(data))
                            serial_port.flushInput()
                    except Exception as e:
                        try:
                            if serial_port is not None and not serial_port.is_open:
                                serial_port.open()
                        except Exception as e:
                            pass
                        logger.error(f"Error in sending data {e}", exc_info=True)
            
            message = await websocket.receive_text()
            if message == 'R':
                try:
                    logger.info(f"Received message Socket {message}", exc_info=True)
                    serial_port.write(bytes(message, 'utf-8'))
                    serial_port.flush()
                    data = serial_port.readline()
                    data = data.decode()
                    if data != '':
                        logger.info("Received Data from Serial Port: {}".format(data))
                    serial_port.flushInput()                    
                except Exception as e:
                    logger.error(f"Error in sending data {e}", exc_info=True)
            else:
                logger.info(f"Received message from Socket {message}", exc_info=True)
                
                if message == 'train':
                    logger.info(f"Start Training new dataset")
                    subprocess.Popen(["python", "training.py"])
            
            if message.isnumeric():
                try:
                    serial_port.write(bytes(message, 'utf-8'))
                    serial_port.flush()
                    logger.info(f"Sendig message {message}")
                except Exception as e:
                    logger.error(f"Error in sending data {e}", exc_info=True)
            

    except Exception as e:
        logger.error(f"Error message f{e}", exc_info=True)
        # await websocket.close()


if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=5555, reload=True)