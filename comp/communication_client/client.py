#comp/communication_client/client.py
"""
Client for Computer

TODO: Add documentation
"""

# Imports
import socket

class CommunicationClient:
    """A TCP client for communicating with the server."""
    
    def __init__(self, host, port):
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
        self.running = bool(False)
        self.status = str('WAIT')
        self.timer = bool(False)

    def connect_to_server(self):
        """
        Connect to the server.
        """
        try:
            self.running = True
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
            self.server_socket.settimeout(0.5)
            self.connected = True
        except Exception as error:
            raise RuntimeError(f"Error connecting to server: {error}")
    
    def close_connection(self):
        """Close the connection with the server."""
        if self.connected:
            self.send('quit')
            self.server_socket.close()
            print("Connection closed")
            
    def send(self, data):
        """
        Send encoded bytes to the server.
        """
        try:
            if self.connected:
                if data is not None:
                    self.server_socket.sendall(len(data).to_bytes(4, 'big'))
                    self.server_socket.sendall(data)
                else:
                    pass
        except socket.error as error:
            raise RuntimeError(f"Error sending data: {error}")

    def receive(self):
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

        except socket.timeout:
            #print("Receive operation timed out.")
            return None

        except socket.error as error:
            raise RuntimeError(f"Error receiving data: {error}")

    def PING(self):
        """
        Send PING message to the server.
        """
        self.send('PING'.encode())
        self.setPING()

    def PONG(self):
        """
        Send PONG message to the server.
        """
        self.send('PONG'.encode())
        self.setPONG()

    def checkStatus(self):
        """
        Status of the timer, waits for 'PING' 
        
        Args: data: 'PING' or 'PONG' for init, images or commands/data respectively
        """
        try:
            if self.status == 'WAIT':
                data = (self.receive()).decode()
                if data == 'PONG':
                    self.status = 'PONG'
                elif data == 'PING':
                    self.status = 'PONG'
                    
                self.timer = True
                
            if self.status == 'PING':
                self.timer = True
                if (self.receive()).decode() == 'PONG':
                    self.timer = False
                    self.status = 'PONG'
            
            if self.status == 'PONG':
                self.timer = False
                self.status = 'WAIT'
            
        except Exception as error:
            raise error
        
    def setPING(self):
        self.status = 'PING'

    def setPONG(self):
        self.status = 'PONG'
        
    def setWAIT(self):
        self.status = 'WAIT'