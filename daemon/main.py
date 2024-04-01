#main controller for Pi (daemon)

import sys
import time

from camera.camera_controller import ThermalCamera, BasicUSBcamera
import communication_server as server

# Global variables
host = "192.168.10.174"  # Raspberry Pi IP address
port = 12345  # Chosen port number
cam1 = 0
therm1 = 1
therm2 = 2



def main():
    pass



#if __name__ == "__main__":
    #try:
       #while(not connected)
            #wait for connection 
       #Send PING/ send init satus 
       #While timer running
            #wait for PONG
       #While(GCODE START COMMAND OR NOT DEBUG MODE SET) 
            #wait for GCODE start
       #Send PING GCODE START
       #SEND CAMERA CALLIBRATION DATA
       #WAIT FOR PONG
       #READ GCODE FROM SERIAL 
       #WHILE(NOT GCODE END)
            #IF GCODE FLAG
                #SEND PING/GCODE FLAG
                #WAIT FOR PING
                #READ COMMAND
                #PROCESSS COMMAND
                #SEND NECCESARRY DATA
                #SEND PONG
                #WAIT FOR PING
                #READ COMMAND
                #PROCESS COMMAND
                #SEND OK
                #SEND PONG
           #ELSE
               #READ GCODE FROM SERIAL         
    #except Exception as error:
        #PROCESS ERROR
        #PRINT ERROR(SEND TO CLIENT MAYBE)

if __name__ == "__main__":
    try:
       myServer = server.CommunicationServer(host, port)
       myServer.start_server()
       while (not myServer.connected):
           time.sleep(0.1)
       
       #INITIALIZE EVEYRTHING ANS CHEKC CONNECTION
       initStatus = 0    
       myServer.send()    

    except Exception as error:
        print(f"Error starting server: {error}")
        sys.exit(1)



#OLD
if __name__ == "__main__":
    try:
        server.server_startup(host, port)
        server.server_begin()
    except Exception as error:
        print(f"Error starting server: {error}")
        sys.exit(1)
