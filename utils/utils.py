import logging
import serial.tools.list_ports
from typing import List

def get_logger(environment: str = "DEV", name: str = __name__) -> logging.getLogger:
    logger = logging.getLogger(name)
    
    
    if environment != "DEV":
        raise NotImplementedError("Only DEV environment is supported")
    
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(process)d] %(levelname)s : %(message)s', datefmt='%Y-%m-%dT%H:%M:%S %Z')
    logger_handler = logging.StreamHandler()
    logger_handler.setFormatter(formatter)
    logger.addHandler(logger_handler)
    return logger


def get_serial_ports() -> List[serial.tools.list_ports.comports]:
    ports = list(serial.tools.list_ports.comports())
    if len(ports) < 1:
        raise Exception("No serial ports found")
    return ports

# for port, desc, hwid in sorted(ports):
#         print("{}: {} [{}]".format(port, desc, hwid))