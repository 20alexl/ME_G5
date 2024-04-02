#
"""
Main Controller for Computer(comp)
"""


#IMPORTS
from pydoc import cli
import time
import sys
import cv2

#CUSTOME CLASSES
import processing as processing
import communication_client as client



def start():
    """
    MAIN INITIALIZATION
    """


    try:    
        #Global Flags
        initPassed = False
        printerFlag = 0
        DEBUG = True
        pinged = False

        # Global variables
        initStatus = '404'
        host = "192.168.10.174"  # Raspberry Pi IP address
        port = 12345  # Chosen port number
    
        myCommand = None
        myData = None
        layer = 0
        
    

        #Global Instances
        myTimer = client.timing.Timer()
        myClient = client.client.CommunicationClient(host, port, myTimer)
        myProcess = processing.process.ImageProcess()

        #connect to server
        myClient.connect_to_server()

        if myClient.connected:
            init_test() #TEST CONNECTION
            if initPassed:#IF TEST PASSED
                myTimer.checkStatus(myClient) #start timer
                while myTimer.running:
                    myTimer.checkStatus(myClient) #recieive ping
                    server_inti_status = (client.by2com(myClient.receive())) #RECIEVE TEST INIT STATUS
            
            if server_inti_status == initStatus:
                if DEBUG:
                    debug()#RUN DEBUG MODE
                else:
                     main()#RUN MAIN LOOP
             
    except Exception as error:
        raise error


    """
    MAIN LOOP
    """



    def main():
        try:    
            while(myClient.connected):   
                if client.by2com(myClient.receive()) == 'PING':#IF PING RECIEVED:(MEANING FLAG WILL BE SENT)
                    myCommand = readFlag(client.by2com(myClient.receive())) #PROCESS FLAG:(USUALLY LAYER OR START/STOP) RETURNS COMMAND:(USUALLY GET)
                        
                    myClient.PONG() #SEND PONG TO INDICATE FLAG COMMAND READY
                    myClient.send(client.com2by(myCommand)) #SEND COMMAND
                    wait() #WAIT FOR PONG:(READY FOR RESPONSE)
                        
                    myData = readData(myClient.receive()) #PROCESS DATA:(USUALLY IMAGE or STR) RETURNS DECODED DATA:(USUALLY IMAGE)
                    myCommand = process(myData)#PROCESS DATA:(USALLY IMAGE) RETURNS COMMAND:(USUALLY SET)
                    
                    myClient.PONG() #SEND PONG TO INDICATE PROCESS COMMAND READY
                    myClient.send(client.com2by(myCommand)) #SEND COMMAND

        except Exception as error:
            raise error
        


    """
    FUNCTIONS
    """
           
        
    #INITIALIZATION TEST
    def init_test():
        try:
            if myClient.connected:
                client.test(myClient, myTimer)
            initPassed = True
            initStatus = '200'
        except Exception as error:
            raise error         
      
        
    #RESET EXCEPTIONS    
    def reset():
        try:
            if myClient.connected:
                time.sleep(1)
                send = input("Do you want to restart the Server? (y/n) ")
                if send == 'y':
                    myClient.PING()
                    myClient.send(client.com2by('QUIT'))
                    myClient.send(client.com2by(send))
                if input("Do you want to restart the Client? (y/n) ") == 'y':
                    stop()
                    start()
                else:
                    stop()
                    exit
        except Exception as error:
            raise error
  
        
    #WAIT FOR TIMER
    def wait():
        try:
            myTimer.checkStatus(myClient)
            while(myTimer.running == True):
                myTimer.checkStatus(myClient)
        except Exception as error:
            raise error
      
        
    #READ FLAGS
    def readFlag(flag):
        try:
            printerFlag = flag
            #FLAGS: 0=NONE, 1=CALIBRATION DATA, 2=LAYER CHANGE, 3=SEND COMMAND
            if printerFlag == 'RESET':
                reset()
            else:
                if flag > 0:
                    if flag == 0:
                        return None
                    elif flag == 1:
                        #get calibration data
                        command = myProcess.calibrate()
                        return command
                    elif flag == 2:
                        #get layer data
                        command = myProcess.layer_change()
                        return command
                    elif flag == 3:
                        #get degub command
                        return input ("Enter command: ")
                    else:
                        return None
                else:
                    raise RuntimeError(f"Invalid flag: {flag}")
        except Exception as error:
            raise RuntimeError(f"Error reading flag: {error}")
    

    #READ DATA
    def readData(data):
        try:
            # Check if the data starts with the JPEG magic number
            if data.startswith(b'\xff\xd8\xff'):
                return client.by2im(data)
            else:
                return client.bytocom(data)
        except Exception as error:
            raise RuntimeError(f"Error reading data: {error}")
    

    #PROCESS DATA
    def process(data):
        try:
            if data is not None:
                myProcess.process(data)
            else:
                pass
        except Exception as error:
            raise RuntimeError(f"Error reading flag: {error}")
    

    #STOP ALL PROCESSES
    def stop():
        try:
            if myClient.connected:
                myClient.close_connection()
            #myPrinter.disconnect()
        except Exception as error:
            raise error


    """
    DEBUG LOOP
    """
    

    def debug():
        while True:
            try:
                if myClient.connected:
                    if client.by2com(myClient.receive()) != 'PING':
                        reset()
                    else:
                        myCommand = readFlag(3) #PROCESS FLAG RETURNS COMMAND (USUALLY GET)
                            
                        myClient.PING() #SEND PING TO INDICATE FLAG COMMAND
                        myClient.send(client.com2by(myCommand)) #SEND FLAG
                        wait() #WAIT FOR PONG(READY FOR RESPONSE)
                            
                        myData = readData(client.by2com(myClient.receive())) #PROCESS DATA RETURNS COMMAND (USUALLY SET)
                        process(myData)
            except Exception as error:
                raise error


#MAIN
if __name__ == "__main__":
    try:
        start()
    except Exception as error:
        print(f"Error: {error}")
        """
        try:
            start.reset()
        except Exception as error:
            raise error
        print(f"{error}")
        """
        sys.exit(1)