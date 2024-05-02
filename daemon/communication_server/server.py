#daemon/communication_server/server.py
"""
Server for the Raspberry Pi

TODO: Add documentation
"""

# Imports
import serial
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
        self.connected = bool(False)
        self.running = bool(False)
        self.status = str('WAIT')
        self.timer = bool(False)

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
                self.client_socket.settimeout(0.2)
                self.server_socket.settimeout(0.2)
                self.connected = True

        except socket.error as error:
            raise RuntimeError(f"Error Starting server: {error}")


    def stop_server(self):
        """
        Stop the server and close the connection with the client.
        """
        try:
            if self.connected:
                self.send(b"STOP Server stopped or reset")
                self.client_socket.close()
                self.server_socket.close()
                self.connected = False
                print("Server stopped")
                self.running = False
                self.status = 'STOP'

        except socket.error as error:
            raise RuntimeError(f"Error stopping server: {error}")


    def send(self, data):
        """
        Send encoded bytes to the client.
        """
        try:
            if self.connected:
                self.setPING()
                if data is not None:
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
                length_data = self.client_socket.recv(4)
                length = int.from_bytes(length_data, 'big')
                data = b''
                while len(data) < length:
                    data += self.client_socket.recv(length - len(data))
                print("REC " + data.decode())
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
        self.send(b'PING')
        self.setPING()

    def PONG(self):
        """
        Send PONG message to the client.
        """
        self.send(b'PONG')
        self.setPONG()

    def checkStatus(self):
        """
        Status of the timer, waits for 'PING' 
        
        Args: data: 'PING' or 'PONG' for init, images or commands/data respectively
        """
        try:
            if self.status == 'STOP':   pass
            else:
                if self.status == 'WAIT':
                    data = self.receive()
                    if data is not None:
                        data = data.decode()
                    if data == 'PONG':
                        self.status = 'PONG'
                        return
                    elif data == 'PING':
                        self.status = 'PONG'
                        return

                    self.timer = True

                if self.status == 'PING':
                    self.timer = True
                    data = self.receive()
                    if data is not None:
                        data = data.decode()
                    if data == 'PONG':
                        self.timer = False
                        #self.status = 'WAIT'
            
                if self.status == 'PONG':
                    self.timer = False
                    #self.status = 'WAIT'

        except Exception as error:
            raise error

    def setPING(self):
        self.status = 'PING'

    def setPONG(self):
        self.status = 'PONG'

    def setWAIT(self):
        self.status = 'WAIT'


    #WAIT FOR TIMER
    def wait(self):
        try:
            #self.server_socket.settimeout(2)
            self.checkStatus()
            while(self.timer):
                self.checkStatus()
                #print("WAITING")
                #print(self.status)

            #self.server_socket.settimeout(0.2)

        except Exception as error:
            raise error
