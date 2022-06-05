import os, sys, time
import random

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
import serial
from utils.utils import get_logger, get_serial_ports

logger =get_logger(name=__name__)

ports = get_serial_ports()
_port = None
serial_port = None

if __name__ == "__main__":
    for port, desc, hwid in sorted(ports):
        logger.info("{}: {} [{}]".format(port, desc, hwid))
        if "USB-Serial" in desc:
            _port = port
            break
    if _port is not None:
        serial_port = serial.Serial(_port, baudrate=9600)
        serial_port.reset_input_buffer()

    while True:
        serial_port.reset_input_buffer()
        try:
            if serial_port.inWaiting() > 0:
                data = serial_port.readline()
                data = data.decode()
                print(data)
                
            if data:
                logger.info("Cleaned message: {}".format(data.strip()))
                if "Ready" in data:
                    finger_id = str(random.randint(1, 127) )
                    logger.info(f"Sending Data to Arduino: {finger_id}")
                    serial_port.write(bytes(finger_id, "utf-8"))
                    serial_port.flush()
                    # serial_port.write('{}'.format(finger_id))
        except Exception as e:
            logger.error(e)
        # time.sleep(0.1)
        # serial_port.close()
        