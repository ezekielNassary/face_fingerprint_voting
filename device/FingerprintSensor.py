import time
from pyfingerprint.pyfingerprint import PyFingerprint
from dataclasses import dataclass
from utils.utils import get_logger
import hashlib
import tempfile

logger = get_logger(name=__name__)
@dataclass
class FingerprintSensor:
    baudrate: int
    com_port: str = "COM3"
    fingerprint_sensor: PyFingerprint = None
    

    def setup_sensor(self):
        try:
            
            self.fingerprint_sensor =  PyFingerprint('/dev/ttyUSB0', self.baudrate, 0xFFFFFFFF, 0x00000000)
            if (self.fingerprint_sensor.verifyPassword() == False):
                raise ValueError('The given fingerprint sensor password is wrong!')
        except Exception as e:
            logger.info('The fingerprint sensor could not be initialized!')
            logger.info(f'Exception message: {e}')
            # exit(1)
    

    def sensor_details(self) -> str:
        return f"{str(self.fingerprint_sensor.getTemplateCount())} - {str(self.fingerprint_sensor.getStorageCapacity())}"
    
    def enroll_fingerprint(self):
        try:
            logger.info('Waiting for finger...')
            while (self.fingerprint_sensor.readImage() == False):
                pass
            logger.info('Downloading image (this might take a while)...')
            self.fingerprint_sensor.downloadImage('./data/fingerprint.bmp')
            logger.info('Converting image to characteristics...')
            self.fingerprint_sensor.convertImage(0x01)
            logger.info('Uploading image...')
            self.fingerprint_sensor.uploadImage(0x01)
            logger.info('Searching for template...')
            result = self.fingerprint_sensor.searchTemplate()
            positionNumber = result[0]
            accuracyScore = result[1]

            if (positionNumber >= 0):
                logger.info('Template already exists at position #' + str(positionNumber))

            logger.info('Remove finger...')
            time.sleep(2)

            logger.info('Waiting for same finger again...')
            
            
            while (self.fingerprint_sensor.readImage() == False):
                pass


            self.fingerprint_sensor.convertImage(0x02)

            if (self.fingerprint_sensor.compareCharacteristics() == 0):
                raise Exception('Fingers do not match')
            
            self.fingerprint_sensor.createTemplate()
            
            
            positionNumber = self.fingerprint_sensor.storeTemplate()
            
        except Exception as e:
            logger.info('Operation failed!')
            logger.info('Exception message: ' + str(e))
            exit(1)
    
    def search_fingerprint(self):
        try:
            logger.info('Waiting for finger...')
            while (self.fingerprint_sensor.readImage() == False):
                pass

            logger.info('Converting image to characteristics...')
            self.fingerprint_sensor.convertImage(0x01)

            logger.info('Searching for template...')
            result = self.fingerprint_sensor.searchTemplate()

            positionNumber = result[0]
            accuracyScore = result[1]

            if (positionNumber == -1):
                logger.info('No match found!')
            else:
                logger.info('Found template at position #' + str(positionNumber))
                logger.info('The accuracy score is: ' + str(accuracyScore))
            
            self.fingerprint_sensor.loadTemplate(positionNumber, 0x01)
            characteristics = self.fingerprint_sensor.downloadCharacteristics(0x01)

            print('SHA-2 hash of template: ' + hashlib.sha256(characteristics).hexdigest())
            
            logger.info('Fingerprint matched!')
        except Exception as e:
            logger.info('Operation failed!')
            logger.info('Exception message: ' + str(e))
            exit(1)

    def delete_fingerprint(self, pos: int):
        try:
            if (self.fingerprint_sensor.deleteTemplate(pos) == True):
                logger.info('Template deleted!')
        except Exception as e:
            logger.info('Operation failed!')
            logger.info('Exception message: ' + str(e))
            exit(1)
    
    def delete_all_fingerprints(self):
        try:
            if (self.fingerprint_sensor.emptyDatabase() == True):
                logger.info('Database cleared!')
        except Exception as e:
            logger.info('Operation failed!')
            logger.info('Exception message: ' + str(e))
            exit(1)
    
    def get_fingerprint_count(self):
        return self.fingerprint_sensor.getTemplateCount()
    
    def download_fingerprint(self):
        try:
            logger.info('Waiting for finger...')
            while (self.fingerprint_sensor.readImage() == False):
                pass

            image_destination = tempfile.gettempdir() + '/fingerprint.bmp'
            logger.info('Downloading image (this might take a while)...')
            self.fingerprint_sensor.downloadImage(image_destination)
        except Exception as e:
            logger.info('Operation failed!')
            logger.info('Exception message: ' + str(e))
            exit(1)
        