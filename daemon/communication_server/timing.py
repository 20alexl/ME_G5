"""
Timers for timing code on the Server (Daemon)
"""

from . import server
import cv2
import numpy as np

class Timer:
    """
    Timer for timing code
    """

    def __init__(self):
        self.running = False
        self.state = 'WAIT'
        self.data = None
    
    #Return server state
    def getState(self):
        return self.state
    
    #Send server state to client
    def sendState(self):
        server.client_socket.sendall(self.state.encode('utf-8'))
    
    #Send PING to client
    def PING():
        server.client_socket.sendall('PING'.encode('utf-8'))
        
    #Send PONG to client
    def PONG():
        server.client_socket.sendall('PONG'.encode('utf-8'))

    #Convert text to bytes
    def com2by(self, data):
        return data.encode('utf-8')
    
    #Convert image to bytes
    def im2by(self, data):
        data = cv2.imencode('.jpg', data)[1].tobytes()
        server.client_socket.sendall(len(data).to_bytes(4, 'big'))
        return data
    
    #Convert bytes to text
    def by2com(self, data):
        return data.decode('utf-8')

    #
    def status(self):
        """
        Status of the timer, waits for 'PING' 
        
        Args: data: 'PING' or 'PONG' for init, images or commands/data respectively
        """
        try:
            if self.state == 'WAIT':
                self.running = False
                return True
                
            elif self.state == 'PING':
                self.running = True
                return False
            
            elif self.state == 'PONG':
                self.running = True
                return False
            
        except Exception as error:
            raise error
            
    #OLD
    def status(self, data):
        """
        Status of the timer, waits for 'PING' 
        
        Args: data: 'PING' or 'PONG' for init, images or commands/data respectively
        """
        try:
            self.sendPong() #SEND PONG
            if (type(data) == 'numpy.ndarray'):
                server.client_socket.sendall(self.im2by(data))
                self.running = True
                while(self.running): 
                    ret = server.client_socket.recv(1024)
                    if ret == 'PING':
                        ret = self.by2com(server.client_socket.recv(1024))
                        self.running = False
                    
                return self.running, ret
            
            elif (type(data) == 'str'):
                server.client_socket.sendall(self.com2by(data))
                self.running = True
                while(self.running):
                    ret = self.by2com(server.client_socket.recv(1024))
                    if ret == 'PONG':
                        ret = self.by2com(server.client_socket.recv(1024))
                        self.running = False
                    
                return self.running, ret
            
            else:
                self.sent = False
                self.ack = False
                self.running = False
                return self.running, None
            
        except Exception as error:
            raise error
            self.running = False
