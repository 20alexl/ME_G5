"""
Timers for timing code on the Server (Daemon)
"""

class Timer:
    """
    Timer for timing code
    """

    def __init__(self):
        self.running = False
        self.state = 'WAIT'
        self.data = None

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
        
    def setPING(self):
        self.state = 'PING'

    def setPONG(self):
        self.state = 'PONG'
        
    def setWAIT(self):
        self.state = 'WAIT'
            
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
