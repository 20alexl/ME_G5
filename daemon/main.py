#main controller for Pi (daemon)
import sys

from camera.camera_controller import ThermalCamera, BasicUSBcamera
from communication_server.server import CommunicationServer

#golbal variables
host = "192.168.10.174"  # Raspberry Pi IP address
port = 12345  # Chosen port number
cam1 = 0
therm1 = 1
therm2 = 2

def main_init():
    cam1 = BasicUSBcamera(cam1)
    #therm1 = ThermalCamera(therm1)
    #therm2 = ThermalCamera(therm2)
    printer = None
    server = CommunicationServer(host, port, cam1, therm1=None, therm2=None, printer=None)
    return server

if __name__ == "__main__":
    server = main_init()
    server.start_server()
    
