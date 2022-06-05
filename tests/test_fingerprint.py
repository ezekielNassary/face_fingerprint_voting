import unittest


import os,sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from device.FingerprintSensor import FingerprintSensor
from utils.utils import get_logger, get_serial_ports

logger =get_logger(name=__name__)

class TestFingerprint(unittest.TestCase):

    fingerprint = FingerprintSensor()

    @classmethod
    def setUpClass(cls):
        get_comm_ports = get_serial_ports()
        serial_port = None
        for port, desc, hwid in sorted(get_comm_ports):
            if "USB-Serial" in desc:
                serial_port = port
                break
        if serial_port is not None:
            cls.fingerprint = FingerprintSensor(serial_port)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_serial_ports(self):
        ports = get_serial_ports()

        logger.info("Received Ports {}".format(ports))
        self.assertTrue(len(ports) > 0)