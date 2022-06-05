#!/usr/bin/env python3

import asyncio
import websockets
import threading
import time
import random
import os, sys


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from utils.utils import get_logger, get_serial_ports

logger =get_logger(name=__name__)
ports = get_serial_ports()

async def send(client, data):
    await client.send(data)

async def handler(client, path):
    # Register.
    logger.info("Websocket Client Connected.", client)
    clients.append(client)
    while True:
        try:
            pong_waiter = await client.ping()
            await pong_waiter
        except Exception as e:
            clients.remove(client)
            logger.info("Websocket Client Disconnected", client)
            break

clients = []
start_server = websockets.serve(handler, "", 5555)

asyncio.get_event_loop().run_until_complete(start_server)
threading.Thread(target = asyncio.get_event_loop().run_forever).start()

print("Socket Server Running. Starting main loop.")

async def get_message(client):

    try:
        message = await client.recv()
        logger.info(f"Websocket Client Message Received. {message}", exc_info=True)

        asyncio.gather(*[send(client, f"{message}") for client in clients])

        if message is None:
            pass
    except Exception as e:
        pass


while True:
    # data = str(gen_data())
    message_clients = clients.copy()
    logger.info(f"Websocket Client Message Received. {message_clients}", exc_info=True)
    
    for _client in message_clients:
        try:
            pass
            asyncio.run(get_message(_client))
            # asyncio.run(send(client, 1))
        except Exception as e:
            print(e)
            # Clients might have disconnected during the messaging process,
            # just ignore that, they will have been removed already.
            pass