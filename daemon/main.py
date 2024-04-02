#main controller for Pi (daemon)

import sys


import camera as camera
import communication_server as server



def start():
    try:    
        #Global Flags
        initPassed = False
        initStatus = '404ERROR'
        DEBUG = True

        # Global variables
        host = "192.168.10.174"  # Raspberry Pi IP address
        port = 12345  # Chosen port number
        cam1 = 0
        therm1 = 1
        therm2 = 2
    

        #Global Instances
        myTimer = server.timing.Timer()
        myServer = server.server.CommunicationServer(host, port, myTimer)
        #myPrinter = printer.printer_controller.Communication()
        cam1 = camera.camera_controller.BasicUSBcamera(cam1)
        #therm1 = camera.camera_controller.ThermalCamera(therm1)
        #therm2 = camera_controller.ThermalCamera(therm2)
    
        myServer.start_server()

        if myServer.connected:
            init_test()
            if initPassed:
                myServer.PING()
                myServer.send(server.com2by(initStatus))
                
        main()
        

        def init_test():
            try:
                if myServer.connected:
                    myServer.test()
                if cam1 is not None:
                    cam1.test()
                if therm1 is not None:
                    therm1.test()
                if therm2 is not None:    
                    therm2.test()
                #if myPrinter.connected:    
                #    myPrinter.test()
                initPassed = True
                initStatus = '200OK'
            except Exception as error:
                raise error
            
    
        def main():
            try:    
                #while(printer not end gcode or DEBUG):
                while(DEBUG):    
                    #printer.get_printer_state()
                    if printer.flag == True
                        Send server
                        Send Flag Value
                        Wait for Ping
                        printer.flag = False
            except Exception as error:
                raise error
                    

        def reset():
            try:
                
            except Exception as error:
                raise error

    except Exception as error:
        raise error




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
        start()
    except Exception as error:
        print(f"Error: {error}")
        try:
            start.reset()
        except Exception as error:
            raise error
        print(f"{error}")
        sys.exit(1)