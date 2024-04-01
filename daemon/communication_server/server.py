"""
Server for the Raspberry Pi

TODO: Add documentation
"""

# Imports
import socket
import cv2
import numpy as np
import struct
import sys
import threading
import time

from . import timing


class CommunicationServer:
    """A TCP server for handling communication with clients."""   

    def __init__(self, host, port):
        """
        Initialize the CommunicationServer.
        
        Args:
            host (str): The IP address of the server.
            port (int): The port number to listen on.
            cam1: An instance of BasicUSBcamera representing the USB camera.
            therm1: An instance of ThermalCamera representing thermal camera 1.
            therm2: An instance of ThermalCamera representing thermal camera 2.
            printer: An instance representing the printer (currently not used).
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.connected = False
        self.error = None

    def start_server(self):
        """
        Start the server and listen for incoming connections.
        """
        try: 
            if not self.connected:    
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.server_socket.bind((self.host, self.port))
                self.server_socket.listen(1)
                print(f"Server listening on {self.host}:{self.port}")
                self.client_socket, client_address = self.server_socket.accept()
                self.connected = True
            
                #while self.running:
                #    self.client_socket, client_address = self.server_socket.accept()
                #    print(f"Connection established with {client_address}")
                #    self.handle_client(self.client_socket)
           
        except Exception as error:
            self.error = error
            raise error
            #print(f"Error starting server: {error}")


    def stop_server(self, client_socket):
        """
        Stop the server and close the connection with the client.
        
        Args:
            client_socket: The socket object representing the client connection.
        """
        if self.connected:
            time.sleep(0.5)
            client_socket.close()
            time.sleep(1.5)
            self.server_socket.close()
            self.connected = False
            self.server_socket = None
            print("Server stopped")

    #Sends encoded bytes
    def send(self, data):
        self.client_socket.sendall(data)
    
    #Returns recivied bytes
    def rec(self):
        return self.client_socket.recv(1024)
