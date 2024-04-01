"""
Timers for timing code on Computer (Comp)
"""

from . import client
import cv2
import numpy as np

class Timer:
    """
    Timer for timing code
    """

    def __init__(self):
        self.running = False
        
    def sendPong():
        client.client_socket.sendall('PONG'.encode('utf-8'))
    
    def com2by(self, data):
        return data.encode('utf-8')
    
    def im2by(self, data):
        data = cv2.imencode('.jpg', data)[1].tobytes()
        client.client_socket.sendall(len(data).to_bytes(4, 'big'))
        return data

    def by2im(self, data):
        return cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    
    def by2com(self, data):
        return data.decode('utf-8')

    def status(self, data):
        """
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
