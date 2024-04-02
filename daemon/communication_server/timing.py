"""
Timers for timing code on the Server (Daemon)
"""

from telnetlib import EL


class Timer:
    """
    Timer for timing code
    """

    def __init__(self):
        self.running = False
        self.state = 'WAIT'
        self.data = None

    #
    def checkStatus(self, server):
        """
        Status of the timer, waits for 'PING' 
        
        Args: data: 'PING' or 'PONG' for init, images or commands/data respectively
        """
        try:
            if self.state == 'WAIT':
                data = (server.receive()).decode()
                if data == 'PONG':
                    self.state = 'PONG'
                elif data == 'PING':
                    self.state = 'PING'
                    
                self.running = True
                
            if self.state == 'PING':
                self.running = True
                if (server.receive()).decode() == 'PONG':
                    self.state = 'PONG'
            
            if self.state == 'PONG':
                self.running = False
                self.state = 'WAIT'
            
        except Exception as error:
            raise error
        
    def setPING(self):
        self.state = 'PING'

    def setPONG(self):
        self.state = 'PONG'
        
    def setWAIT(self):
        self.state = 'WAIT'
            
