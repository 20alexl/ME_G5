#daemon/communication_server/server.py
"""
Server for the Raspberry Pi

TODO: Add documentation
"""

# Imports
import socket


class CommunicationServer:
    """A TCP server for handling communication with clients."""   

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
        self.client_socket = None
        self.connected = False
        self.running = False
        self.state = 'WAIT'
        self.timer = False

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
                self.running = True
                print(f"Server listening on {self.host}:{self.port}")
                self.client_socket, client_address = self.server_socket.accept()
                self.client_socket.settimeout(0.5)
                self.connected = True
        except socket.error as error:
            raise RuntimeError(f"Error Starting server: {error}")


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
                self.running = False
                self.status = 'None'
        except socket.error as error:
             raise RuntimeError(f"Error stopping server: {error}")

    def send(self, data):
        """
        Send encoded bytes to the client.
        """
        try:
            if self.connected:
                if data:
                    self.client_socket.sendall(len(data).to_bytes(4, 'big'))
                    self.client_socket.sendall(data)
                else:
                    pass
        except socket.error as error:
            raise RuntimeError(f"Error sending bytes {len(data)}: {error}")

    def receive(self):
        """
        Receive bytes from the client.
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
        Send PING message to the client.
        """
        self.send('PING'.encode())
        self.setPING()

    def PONG(self):
        """
        Send PONG message to the client.
        """
        self.send('PONG'.encode())
        self.setPONG()
        
    def checkStatus(self):
        """
        Status of the timer, waits for 'PING' 
        
        Args: data: 'PING' or 'PONG' for init, images or commands/data respectively
        """
        try:
            if self.state == 'WAIT':
                data = (self.receive()).decode()
                if data == 'PONG':
                    self.state = 'PONG'
                elif data == 'PING':
                    self.state = 'PING'
                    
                self.timer = True
                
            if self.state == 'PING':
                self.timer = True
                if (self.receive()).decode() == 'PONG':
                    self.timer = False
                    self.state = 'PONG'
            
            if self.state == 'PONG':
                self.timer = False
                self.state = 'WAIT'
            
        except Exception as error:
            raise error
        
    def setPING(self):
        self.state = 'PING'

    def setPONG(self):
        self.state = 'PONG'
        
    def setWAIT(self):
        self.state = 'WAIT'

