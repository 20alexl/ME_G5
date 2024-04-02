"""
Server for the Raspberry Pi

TODO: Add documentation
"""

# Imports
import socket

class CommunicationClient:
    """A TCP client for communicating with the server."""
    
    def __init__(self, host, port, timer):
        """
        Initialize the CommunicationServer.
        
        Args:
            host (str): The IP address of the server.
            port (int): The port number to listen on.
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.connected = False
        self.timer = timer

    def connect_to_server(self):
        """
        Connect to the server.
        """
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
            self.connected = True
        except Exception as error:
            raise Exception(f"Error connecting to server: {error}")
    
    def close_connection(self):
        """Close the connection with the server."""
        if self.connected:
            self.send_command('quit')
            self.server_socket.close()
            print("Connection closed")
            
    def send(self, data):
        """
        Send encoded bytes to the server.
        """
        try:
            if self.connected:
                self.server_socket.sendall(data)
        except socket.error as error:
            raise RecursionError(f"Error sending data: {error}")
        
    def receive(self):
        """
        Receive bytes from the server.
        """
        try:
            if self.connected:
                return self.server_socket.recv(1024)
        except socket.error as error:
            raise RecursionError(f"Error receiving data: {error}")
        
    def receiveImage(self):
        """
        Receive bytes from the server.
        """
        try:
            if self.connected:
                length_data = self.server_socket.recv(4)
                length = int.from_bytes(length_data, 'big')
                data = b''
            
                while len(data) < length:
                    data += self.server_socket.recv(length - len(data))
                return data
        except socket.error as error:
            raise RecursionError(f"Error receiving data: {error}")
        
    def PING(self):
        """
        Send PING message to the server.
        """
        self.send('PING'.encode())
        self.timer.setPING()

    def PONG(self):
        """
        Send PONG message to the server.
        """
        self.send('PONG'.encode())
        self.timer.setPONG()
