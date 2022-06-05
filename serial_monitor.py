import os, sys
import asyncio
import serial
import threading
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from utils.utils import get_logger, get_serial_ports
import websockets
# websocket.enableTrace(True)
import nest_asyncio
nest_asyncio.apply()

logger =get_logger(name=__name__)
ports = get_serial_ports()

_port = None
serial_port = None
for port, desc, hwid in sorted(ports):
    logger.info("{}: {} [{}]".format(port, desc, hwid))
    if "USB-Serial" in desc:
        _port = port
        break



serial_port = serial.Serial(_port, baudrate=9600, timeout=0)

# def on_message(ws, message):
#     logger.info(f"Websocket Client Message Received. {message}")
#     def run(*args):
#         if message == 'R':
#             logger.info(f"Received message Socket {message}")
#             serial_port.write(b'R')
#             serial_port.flush()
#         if message.isnumeric():
#             serial_port.write(bytes(message, 'utf-8'))
#             serial_port.flush()
#             logger.info(f"Sendig message {message}")
#     threading.Thread(target=run).start()
async def socket_client():
    async with websockets.connect('ws://localhost:5555/ws') as websocket:

        while True:
            try:
                async def run():
                        while True:
                            
                            try:
                                if serial_port.inWaiting() > 0 :
                                    data = serial_port.readline()
                                    data = data.decode()
                                    await websocket.send(data)
                                    logger.info("Received Data from Serial Port: {}".format(data))
                                    await asyncio.sleep(0.1)
                            except Exception as e:
                                logger.info(f"Erorr message {e}", exc_info=True)
                                
                                # await  websocket.send("Hello")                                pass
                
                # asyncio.create_task(run())
        
                # loop.(run())
                try:
                    # loop.run_in_executor(None, lambda: asyncio.run(run()))
                    # await asyncio.sleep(0.1)
                    asyncio.create_task(run())
                    await asyncio.sleep(0.1)
                except Exception as e:
                    logger.info(f"Erorr message {e}", exc_info=True)
                # asyncio.gather(run())
                # threading.Thread(target=run).start()
                # asyncio.run(run())                
                message = await websocket.recv()
                logger.info(f"Received message Socket {message}")
                if message == 'R':
                    logger.info(f"Received message Socket {message}")
                    time.sleep(1)
                    try:
                        serial_port.write(b'R')
                        serial_port.flush()
                    except Exception as e:
                        logger.info(f"Erorr message {e}", exc_info=True)
                if message.isnumeric():
                    try:
                        serial_port.write(bytes(message, 'utf-8'))
                        serial_port.flush()
                        logger.info(f"Sendig message {message}")
                    except Exception as e:
                        logger.info(f"Erorr message {e}", exc_info=True)
                                        
            except Exception as e:
                logger.info(f"Erorr reading message {e}", exc_info=True)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(socket_client())
    # wsapp = websocket.WebSocketApp("'ws://localhost:5555/ws'", on_message=on_message)
    # wsapp.run_forever()

    while True:
        try:
            if serial_port.inWaiting() > 0 :
                data = serial_port.readline()
                data = data.decode()
                logger.info("Received Data from Serial Port: {}".format(data))
                # wsapp.send(data)
        except Exception as e:
            pass