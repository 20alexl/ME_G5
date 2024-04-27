#comp/main.py
"""
Main Controller for Computer(comp)
"""

#IMPORTS
import time
import sys
import cv2

#CUSTOME CLASSES
import processing as processe
import communication_client as client

"""
MAIN CONTROLLER CLASS
"""

class main:
    #INIT
    def __init__(self, host, port):
        """
        Initialize the main controller.
        """

        #Global Instances
        self.myClient = client.client.CommunicationClient(host, port)
        self.myProcess = processe.process.ImageProcess()

        self.myCommand = str
        self.myData = bytes

        self.initPassed = bool(False)
        self.initStatus = "404"
        self.server_init_status = "101"
        self.printerFlag = str(None)

        self.layer = int(0)


    #START
    def start(self):
        try:
            self.myClient.connect_to_server()
            if self.myClient.running:
                while not self.myClient.connected:
                    pass

        except Exception as error:
            raise RuntimeError(f"Error Start Main: {error}")

        
    #STOP
    def stop(self):
        try:
            if self.myClient.running:
                while self.myClient.connected:
                    self.myClient.close_connection()
                    
        except Exception as error:
            raise RuntimeError(f"Error Stop Main: {error}")
    

    #RESET
    def reset(self):
        try:
            if self.myClient.connected:
                    self.stop()
                    exit
        except Exception as error:
            raise RuntimeError(f"Error Reset Main: {error}")
    

    #INITIALIZATION TEST
    def init_test(self):
        try:
            if self.myClient.connected:
                self.initPassed = True
                self.initStatus = "200"
        except Exception as error:
            raise error


    #READ FLAGS
    def readFlag(self, flag):
        try:
            if flag is None:    return   
            self.printerFlag = flag.split(' ', 1)
            #FLAGS: 0=NONE, 1=CALIBRATION DATA, 2=LAYER CHANGE, 3=SEND COMMAND
            if self.printerFlag[0] == 'RESET':
                self.reset()
            else:
                if len(self.printerFlag) > 0:
                    if self.printerFlag[0] == "INIT":
                        #get calibration data
                        self.myProcess.calibrate_data(self.printerFlag[1])
                    elif self.printerFlag[0] == "LAYER":
                        #get layer data
                        self.myCommand = self.myProcess.layer_change(self.printerFlag[1]) #GET IMAGE COMMAND
                    elif self.printerFlag[0] == "TEST":
                        #get degub command
                        self.myCommand = input ("Enter command: ")
                else:
                    raise RuntimeError(f"Invalid flag: {flag}")
        except Exception as error:
            raise RuntimeError(f"Error reading flag: {error}")
    

    #READ DATA
    def readData(self, data):
        try:
            # Check if the data starts with the JPEG magic number
            if self.myCommand is not None:
                command_parts = self.myCommand.split()
                if command_parts[1] == 'image':
                    self.data = client.by2im(data, command_parts[2])
                    print("GOT IMAGE")

                elif command_parts[1] == 'printer':
                    self.data = client.by2com(data)
                    print("GOT DATA")

        except Exception as error:
            raise RuntimeError(f"Error reading data: {error}")
    

    #PROCESS DATA
    def process(self):
        try:
            if self.data is not None:
                self.myProcess.display_image(self.data)
                #self.myProcess.LWOI_AMP(self.myData, self.printerFlag)  
            else:
                pass
        except Exception as error:
            raise RuntimeError(f"Error processing flag: {error}")


    """
    DEBUG LOOP
    """
    

    def debug(self):
        try:
            self.start()

            if self.myClient.connected:
                self.init_test() #TEST ALL CONNTECTED COMPONENTS
            print("Tested!")
            if self.initPassed:#IF ALL TESTS PASS
                self.myClient.wait()#WAIT FOR PING
                self.server_init_status = (client.by2com(self.myClient.receive())) #RECIEVE TEST INIT STATUS
                self.myClient.PONG() #SEND PONG ?
            if self.initStatus == self.server_init_status:
                print("Passed!" + self.initStatus + " : " + self.server_init_status)
            else:
                print("Failed!" + self.initStatus + " : " + self.server_init_status)

            while(self.myClient.running):
                if self.myClient.connected:
                    print("FLAG")
                    self.readFlag("TEST") #PROCESS FLAG RETURNS COMMAND (DEGUB)

                    self.myClient.PING() #SEND PING TO INDICATE FLAG COMMAND

                    print("FLAG")
                    self.myClient.send(client.com2by(self.myCommand)) #SEND COMMAND
                    print("FLAG")
                    self.myClient.wait() #WAIT FOR PONG(READY FOR RESPONSE)

                    self.readData(self.myClient.receive()) #PROCESS DATA RETURNS COMMAND (DEGUB)
                    self.myClient.PONG() #SEND PING TO INDICATE FLAG COMMAND
                    self.process()
        except Exception as error:
            print(f"Error Debugging: {error}")
            sys.exit(1)
            


    """
    MAIN LOOP
    """

    def main(self):
        try:
            self.start()
        

            while(self.myClient.connected):
                self.myClient.checkStatus() #START WIAIT FOR SOMETHING FROM SERVER (USUALLY "PING")   
                if self.myClient.status != 'WAIT':#IF PING RECIEVED:(MEANING FLAG WILL BE SENT)
                    self.readFlag(client.by2com(self.myClient.receive())) #PROCESS FLAG:(USUALLY LAYER OR START/STOP) RETURNS COMMAND:(USUALLY GET)

                    self.myClient.PONG() #SEND PONG TO INDICATE FLAG COMMAND READY
                    self.myClient.send(client.com2by(self.myCommand)) #SEND COMMAND
                    self.myClient.wait() #WAIT FOR PONG:(READY FOR RESPONSE)

                    self.readData(self.myClient.receive()) #PROCESS DATA:(USUALLY IMAGE or STR) RETURNS DECODED DATA:(USUALLY IMAGE)
                    self.process()#PROCESS DATA:(USALLY IMAGE) RETURNS COMMAND:(USUALLY SET)

                    self.myClient.PONG() #SEND PONG TO INDICATE PROCESS COMMAND READY
                    self.myClient.send(client.com2by(self.myCommand)) #SEND COMMAND

        except Exception as error:
            print(error)
            sys.exit(1)


#MAIN
if __name__ == "__main__":
    """
    MAIN INITIALIZATION
    """
    DEBUGGING = True
    #host = "10.0.2.15"  # Raspberry Pi IP address
    host = "192.168.10.191"  # Raspberry Pi IP address
    port = 12345  # Chosen port number
    
    myMain = main(host, port)
    if DEBUGGING:
        myMain.debug() #DEBUG
    else:
        myMain.main() #MAIN