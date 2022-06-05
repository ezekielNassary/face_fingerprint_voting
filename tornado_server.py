import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
from tornado.options import define, options
from utils.utils import get_logger, get_serial_ports
import time
import multiprocessing
 

logger =get_logger(name=__name__)
define("port", default=8080, help="run on the given port", type=int)
 
clients = []

import serial
import time
import multiprocessing

ports = get_serial_ports()
_port = None
serial_port = None

for port, desc, hwid in sorted(ports):
        logger.info("{}: {} [{}]".format(port, desc, hwid))
        if "USB-Serial" in desc:
            _port = port
            break

## Change this to match your local settings
SERIAL_PORT = _port
SERIAL_BAUDRATE = 9600

input_queue = multiprocessing.Queue()
output_queue = multiprocessing.Queue()

class SerialProcess(multiprocessing.Process):
 
    def __init__(self, input_queue, output_queue):
        multiprocessing.Process.__init__(self)
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.sp = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE)
 
    def close(self):
        self.sp.close()
 
    def writeSerial(self, data):
        self.sp.write(data)
        time.sleep(1)
        
    def readSerial(self):
        return self.sp.readline().decode()
 
    def run(self):
 
        self.sp.flushInput()
 
        while True:
            # look for incoming tornado request
            data = self.input_queue.get()
            print("Some data ", data)
            if not self.input_queue.empty():
                data = self.input_queue.get()
 
                # send it to the serial device
                self.writeSerial(data)
                print ("writing to serial: " + data)
 
            # look for incoming serial data
            if (self.sp.inWaiting() > 0):
                data = self.readSerial()
                print ("reading from serial: " + data)
                # send it back to tornado
                self.output_queue.put(data)
 
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
 
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        clients.append(self)
        self.write_message("connected")
 
    def on_message(self, message):
        self.write_message('received from client: %s' % message)
 
    def on_close(self):
        print ('connection closed')
        clients.remove(self)
    
    def check_origin(self, origin):
        return True
## check the queue for pending messages, and rely that to all connected clients
def checkQueue():
    if not output_queue.empty():
        message = output_queue.get()
        for c in clients:
            c.write_message(message)


if __name__ == '__main__':
    ## start the serial worker in background (as a deamon)
    sp = SerialProcess(input_queue, output_queue)
    sp.daemon = True
    sp.start()
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/static/(.*)", tornado.web.StaticFileHandler, {'path':  './'}),
            (r"/ws", WebSocketHandler)
        ]
    )
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(options.port)
    print ("Listening on port:", options.port)

    mainLoop = tornado.ioloop.IOLoop.instance()
    scheduler_interval = 10
    scheduler = tornado.ioloop.PeriodicCallback(checkQueue, scheduler_interval)
    scheduler.start()
    mainLoop.start()