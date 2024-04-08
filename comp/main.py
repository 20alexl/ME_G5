#comp/main.py
"""
Main Controller for Computer(comp)
"""


#IMPORTS
import time
import sys
from tkinter import N
import cv2

#CUSTOME CLASSES
import processing as processing
import communication_client as client



"""
FUNCTIONS
"""
           
        
#INITIALIZATION TEST
def init_test():
    try:
        global initPassed
        global initStatus
        if myClient.connected:
            client.test(myClient, myTimer)
        initPassed = True
        initStatus = "200"
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
                #start()
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
        global printerFlag    
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
                    myProcess.calibrate()
                    return None
                elif flag == 2:
                    #get layer data
                    command = myProcess.layer_change()
                    return command
                elif flag == 3:
                    #get degub command
                    command = input ("Enter command: ")
                    return command
                else:
                    return None
            else:
                raise RuntimeError(f"Invalid flag: {flag}")
    except Exception as error:
        raise RuntimeError(f"Error reading flag: {error}")
    

#READ DATA
def readData():
    try:
        # Check if the data starts with the JPEG magic number
        if myCommand is not None:
            command_parts = myCommand.split()
            if command_parts[1] == 'image':
                data = myClient.receiveImage()
                print("GOT IMAGE")
                return client.by2im(data)
            elif command_parts[1] == 'printer':
                data = myClient.receive()
                print("GOT DATA")
                return client.bytocom(data)
    except Exception as error:
        raise RuntimeError(f"Error reading data: {error}")
    

#PROCESS DATA
def process(data):
    try:
        global myCommand
        global myData
        global layer
        if data is not None:
             myProcess.display_image(data)   
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
    try:
        while(myClient.connected):
            global myCommand
            global myData
            if myClient.connected:
                print("FLAG")
                if client.by2com(myClient.receive()) == 'PING':
                    print("RESET FLAG")
                    reset()
                else:
                    print("FLAG")
                    myCommand = readFlag(3) #PROCESS FLAG RETURNS COMMAND (DEGUB)
                            
                    myClient.PING() #SEND PING TO INDICATE FLAG COMMAND
                    print("FLAG")
                    myClient.send(client.com2by(myCommand)) #SEND COMMAND
                    print("FLAG")
                    wait() #WAIT FOR PONG(READY FOR RESPONSE)
                            
                    myData = readData() #PROCESS DATA RETURNS COMMAND (DEGUB)
                    process(myData)
    except Exception as error:
        raise RuntimeError(f"Error Debugging: {error}")
            

"""
MAIN LOOP
"""



def main():
    try:
        global myCommand
        global myData
        global layer
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



#MAIN
if __name__ == "__main__":
    """
    MAIN INITIALIZATION
    """


    try:    
        #Global Flags
        global initPassed
        global printerFlag
        global DEBUG
        global pinged
        
        initPassed = False
        printerFlag = 0
        DEBUG = True
        pinged = False

        # Global variables
        global server_init_status
        global initStatus
        global host
        global port
        global myCommand
        global myData
        global layer
        
        server_init_status = "101"
        initStatus = "404"
        host = "192.168.10.191"  # Raspberry Pi IP address
        port = 12345  # Chosen port number
    
        myCommand = None
        myData = None
        layer = 0
        
    

        #Global Instances
        print("Initializing...")
        myTimer = client.timing.Timer()
        print("1")
        myClient = client.client.CommunicationClient(host, port, myTimer)
        print("1")
        myProcess = processing.process.ImageProcess()
        print("1")
        print("Initialized!")
        
        #connect to server
        myClient.connect_to_server()
        print("Connected!")
        
        if myClient.connected:
            init_test() #TEST CONNECTION
            print("Tested!")
            if initPassed:#IF TEST PASSED
                myTimer.setWAIT()
                wait() #WAIT FOR PING
                server_init_status = (client.by2com(myClient.receive())) #RECIEVE TEST INIT STATUS
                print("Passed!" + initStatus + " : " + server_init_status)
                    
            if server_init_status == initStatus:
                print("Server Initialization Status: " + server_init_status)
                if DEBUG:
                    debug()#RUN DEBUG MODE
                else:
                    main()#RUN MAIN LOOP
             
    except Exception as error:

        print(f"Error: {error}")

        sys.exit(1)