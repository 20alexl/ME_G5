#main controller for Pi (daemon)

from distutils.cmd import Command
from re import S
from tkinter import SE
from camera.camera_controller import ThermalCamera, BasicUSBcamera
from communication_server.server import CommunicationServer

#golbal variables
host = "192.168.10.174"  # Raspberry Pi IP address
port = 12345  # Chosen port number
cam_top = 0
top = 1
side = 2

def main_init():
    cam1 = BasicUSBcamera(cam_top)
    therm1 = ThermalCamera(top)
    therm2 = ThermalCamera(side)
    printer = None
    server = CommunicationServer(host, port, cam1, therm1=None, therm2=None, printer=None)
    return server

if __name__ == "__main__":
    server = main_init()
    if None:
        server.start_server()
    
