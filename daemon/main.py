#daemon/main.py
"""
Main controller for Pi(daemon)
"""


#IMPORTS
import time
import sys

#CUSTOME CLASSES
import camera as camera
import communication_server as server
import printer as printer
         
"""
MAIN CONTROLLER CLASS
"""


class main:
    #INIT
    def __init__(self, host, port, printer_port=None, cam1=None, therm1=None, therm2=None):
        """
        Initialize the main controller.
        """
        
        #Global Instances
        self.myServer = server.server.CommunicationServer(host, port)#INITIALIZE SERVER(HOST ADRESS, PROT #)
        if printer_port is not None:
            self.myPrinter = printer.printer_controller.PrinterCommunication(printer_port)#INITIALIZE PRINTER(USB PORT)
        else:
            self.myPrinter = None
        if cam1 is not None:
            self.cam1 = camera.camera_controller.BasicUSBcamera(cam1)#INITIALIZE CAMERA(USB PORT)
        else:
            self.cam1 = None
        if therm1 is not None:
            self.therm1 = camera.camera_controller.ThermalCamera(therm1)#INITIALIZE CAMERA(USB PORT)
        else:
            self.therm1 = None
        if therm2 is not None:
            self.therm2 = camera.camera_controller.ThermalCamera(therm2)#INITIALIZE CAMERA(USB PORT)
        else:
            self.therm2 = None
            
        self.myCommand = None
        self.myData = None
        
        self.initPassed = False
        self.initStatus = "404"
        self.printerFlag = False
        self.pinged = False
     
        
    #START
    def start(self):
        try:
            self.myServer.start_server()
            if self.myServer.running:
                while not self.myServer.connected:
                    pass
                    
        except Exception as error:
            raise RuntimeError(f"Error Start Main: {error}")
    

    #STOP
    def stop(self):
        try:
            if self.myServer.running:
                while self.myServer.connected:
                    self.myServer.stop_server()
                #if myPrinter.connected:
                #    myPrinter.disconnect()
                #    pass
                if self.cam1 is not None:
                    self.cam1.release()
                if self.therm1 is not None:
                    self.therm1.release()
                if self.therm2 is not None:    
                    self.therm2.release()
                    
        except Exception as error:
            raise RuntimeError(f"Error Stop Main: {error}")
    

    #RESET
    def reset(self):
        try:
            if self.myServer.connected:
                    self.stop()
                    exit
        except Exception as error:
            raise RuntimeError(f"Error Reset Main: {error}")
    

    #INITIALIZATION TEST
    def init_test(self):
        try:
            if self.cam1 is not None:
                camera.test(self.cam1)
            if self.therm1 is not None:
                camera.test(self.therm1)
            if self.therm2 is not None:    
                camera.test(self.therm2)
            if self.myPrinter.connected:    
                printer.test(self.myPrinter)
            
            self.initPassed = True
            self.initStatus = "200"
        except Exception as error:
            raise error
    

    #WAIT FOR TIMER
    def wait(self):
        try:
           self.myServer.checkStatus()
           while(self.myServer.timer):
                self.myServer.checkStatus()
                print("WAITING")
        except Exception as error:
            raise error
    

    #PROCESS COMMANDS    
    def process(self, command):
        try:
            self.myCommand = command
            command_parts = self.myCommand.split()
            if self.myCommand is not None:
                if len(command_parts) < 1:
                    raise RuntimeError(f"Invalid command format")
                
                command_type = command_parts[0]
                if command_type == 'quit':
                    self.reset() 
                    exit
                    
                device = command_parts[1]
                if command_type == 'get':
                    
                    if device == 'printer':
                        if command_parts[2] == 'pos':
                            #Implement logic to get position
                            self.myData = self.myPrinter.get_position()
                        elif command_parts[2] == 'speed':
                            #Implement logic to get speed
                            self.myData = self.myPrinter.get_speed()
                        elif command_parts[2] == 'temp':
                            #Implement logic to get temperature
                            self.myData = self.myPrinter.get_temp()
                        elif command_parts[2] == 'state':
                            #Implement logic to get state
                            self.myData = self.myPrinter.get_printer_state()
                        elif command_parts[2] == 'flow':
                            #Implement logic to get flow rate
                            self.myData = self.myPrinter.get_flow_rate()
                        else:
                            raise RuntimeError(f"Invalid Printer Command")
                            
                    
                    elif device == 'image':
                    #elif device == 'image':
                        if command_parts[2] == 'cam1':
                            ret, self.myData = self.cam1.capture_frame()
                        elif command_parts[2] == 'therm1':
                            ret, self.myData = self.therm1.capture_frame()
                        elif command_parts[2] == 'therm2':
                            ret, self.myData = self.therm2.capture_frame()
                        else:
                            raise RuntimeError(f"Invalid Image device")
 
                    else:
                        raise RuntimeError(f"Invalid command")
                    
                    if self.myData is not None:  # Check if image data is not None
                        if ret:
                            self.myServer.PONG()
                            self.myServer.send(server.im2by(self.myData))
                            self.wait()
                        elif self.myData.dtype == 'str':
                            self.myServer.PONG()
                            self.myServer.send(server.com2by(self.myData))
                            self.wait()
                        else:
                            raise RuntimeError(f"Invalid Process data type")
                    else:
                        raise RuntimeError(f"Error: Failed to capture data")

                elif command_type == 'set':
                    if device == 'speed':
                        # Implement logic to set speed
                        pass
                    elif device == 'temp':
                        # Implement logic to set temperature
                        pass
                    elif device == 'pos':
                        # Implement logic to set position
                        pass
                    elif device == 'home':
                        # Implement logic to home
                        pass
                    elif device == 'park':
                        # Implement logic to park
                        pass
                    elif device == 'flow':
                        # Implement logic to set flow
                        pass
                    else:
                        raise RuntimeError(f"Invalid device")
                else:
                    raise RuntimeError(f"Invalid command")
            else:
                return None
        except Exception as error:
            raise error
    

    """
    DEGUB LOOP
    """
    
    def debug(self):
        try:
            self.start()
            
            if self.myServer.connected:
                self.init_test() #TEST ALL CONNTECTED COMPONENTS
            print("Tested!")
            if self.initPassed:#IF ALL TESTS PASS
                self.myServer.PING()#SEND PING(INIT PING)
                self.myServer.send(server.com2by(self.initStatus))#SEND INIT STATUS
                self.wait()#WAIT FOR PONG
                print("Passed!" + self.initStatus)
                
            while self.myServer.connected:
                if server.by2com(self.myServer.receive()) == 'PING':
                    print("PINGGED")
                    self.myData = self.process(server.by2com(self.myServer.receive())) #PROCESS COMMAND
                    print("PONGGED")
                    self.myServer.PONG() #SEND PONG (READY TO SEND DATA)
                    self.myServer.send(server.com2by(self.myData)) #SEND DATA
                    print("PONGGED")
        except Exception as error:
            #myServer.PONG()
            #myServer.send(server.com2by(error))
            #myServer.PING()
            print(f"Error Debugging: {error}")
            sys.exit(1)
            

    """
    MAIN LOOP
    """

    def main(self):
        try:
            self.start()
            
            if self.myServer.connected:
                self.init_test() #TEST ALL CONNTECTED COMPONENTS
            print("Tested!")
            if self.initPassed:#IF ALL TESTS PASS
                self.myServer.PING()#SEND PING(INIT PING)
                self.myServer.send(server.com2by(self.initStatus))#SEND INIT STATUS
                self.wait()#WAIT FOR PONG
                print("Passed!" + self.initStatus)
                
            while(self.myServer.connected):
                self.printerFlag = self.myPrinter.get_printer_state() #CHECK FOR SET FLAGS
                if self.printerFlag is not None:
                    self.myServer.PING() #SEND PING TO INDICATE FLAG | TIMER STATE IS PING
                    self.myServer.send(server.com2by(self.myPrinter.flag)) #SEND FLAG
                    self.wait() #WAIT FOR PONG(READY FOR RESPONSE)
                    self.process(server.by2com(self.myServer.receive())) #PROCESS INITIAL COMMAND (USUALY A GET COMMAND)
                    self.process(server.by2com(self.myServer.receive())) #PROCESS SECOND COMMAND (USUALY A SET COMMAND)
                    self.myPrinter.flag = False
        except Exception as error:
            print(error)
            sys.exit(1)
    

#MAIN
if __name__ == "__main__":
    """
    MAIN INITIALIZATION
    """
    DEBUGGING = True
    host = "192.168.10.191"  # Raspberry Pi IP address
    port = 12345  # Chosen port number
    cam1Port = 0
    therm1Port = 1
    therm2Port = 2
    printerPort = 3
    
    myMain = main(host, port, printerPort, cam1Port, None, None)
    if DEBUGGING:
        myMain.debug() #DEBUG
    else:
        myMain.main() #MAIN