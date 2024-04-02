"""
Server for the Raspberry Pi

TODO: Add documentation
"""

# Imports
import socket


class CommunicationServer:
    """A TCP server for handling communication with clients."""   

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
        self.client_socket = None
        self.connected = False
        self.timer = timer

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
        except socket.error as error:
            raise RecursionError(f"Error stopping server: {error}")

    def stop_server(self):
        """
        Stop the server and close the connection with the client.
        """
        try:
            if self.connected:
                self.client_socket.close()
                self.server_socket.close()
                self.connected = False
                print("Server stopped")
        except socket.error as error:
             raise RuntimeError(f"Error stopping server: {error}")

    def send(self, data):
        """
        Send encoded bytes to the client.
        """
        try:
            if self.connected:
                self.client_socket.sendall(data)
        except socket.error as error:
            raise RecursionError(f"Error sending data: {error}")
     
    def sendImage(self, data):
        """
        Send image data to the client.
        """
        try:
            if self.connected:
                self.client_socket.sendall(len(data).to_bytes(4, 'big'))
                self.client_socket.sendall(data)
        except socket.error as error:
            raise RecursionError(f"Error sending image: {error}")

    def receive(self):
        """
        Receive bytes from the client.
        """
        try:
            if self.connected:
                return self.client_socket.recv(1024)
        except socket.error as error:
            raise RecursionError(f"Error receiving data: {error}")

    def PING(self):
        """
        Send PING message to the client.
        """
        self.send('PING'.encode())
        self.timer.setPING()

    def PONG(self):
        """
        Send PONG message to the client.
        """
        self.send('PONG'.encode())
        self.timer.setPONG()
        

