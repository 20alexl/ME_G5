#
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



def start():
    """
    MAIN INITIALIZATION
    """

    try:    
        #Global Flags
        initPassed = False
        printerFlag = False
        DEBUG = True
        pinged = False

        # Global variables
        initStatus = '404'
        host = "192.168.10.174"  # Raspberry Pi IP address
        port = 12345  # Chosen port number
        cam1 = 0
        therm1 = 1
        therm2 = 2
        printer = 3
        
        myCommand = None
        myData = None
        
    

        #Global Instances
        myTimer = server.timing.Timer()
        myServer = server.server.CommunicationServer(host, port, myTimer)#INITIALIZE SERVER(HOST ADRESS, PROT #, myTimer INSTANCE)
        myPrinter = printer.printer_controller.PrinterCommunication(printer)#INITIALIZE PRINTER(USB PORT)
        cam1 = camera.camera_controller.BasicUSBcamera(cam1)#INITIALIZE CAMERA(USB PORT)
        #therm1 = camera.camera_controller.ThermalCamera(therm1)#INITIALIZE THERMAL CAMERA1(USB PORT)
        #therm2 = camera.camera_controller.ThermalCamera(therm2)#INITIALIZE THERMAL CAMERA2(USB PORT)
    
        #START SERVER
        myServer.start_server()


        if myServer.connected:
            init_test() #TEST ALL CONNTECTED COMPONENTS
            if initPassed:#IF ALL TESTS PASS
                myServer.PING()#SEND PING(INIT FLAG)
                myServer.send(server.com2by(initStatus))#SEND INIT STATUS
                
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
            while(myServer.connected):
                myPrinter.get_printer_state() #CHECK FOR SET FLAGS
                if myPrinter.flag == True:
                    myServer.PING() #SEND PING TO INDICATE FLAG | TIMER STATE IS PING
                    myServer.send(server.com2by(myPrinter.flag)) #SEND FLAG
                    wait() #WAIT FOR PONG(READY FOR RESPONSE)
                    process(server.by2com(myServer.receive())) #PROCESS INITIAL COMMAND (USUALY A GET COMMAND)
                    process(server.by2com(myServer.receive())) #PROCESS SECOND COMMAND (USUALY A SET COMMAND)
                    myPrinter.flag = False
        except Exception as error:
            raise error
        


    """
    FUNCTIONS
    """
    

    #INITIALIZATION TEST
    def init_test():
        try:
            if myServer.connected:
                server.test(myServer, myTimer)
            if cam1 is not None:
                camera.test(cam1)
            if therm1 is not None:
                camera.test(therm1)
            if therm2 is not None:    
                camera.test(therm2)
            if myPrinter.connected:    
                printer.test(myPrinter)
            initPassed = True
            initStatus = '200'
        except Exception as error:
            raise error
                              
    
    #RESET EXCEPTIONS    
    def reset():
        try:
            if myServer.connected:
                time.sleep(1)
                myServer.PING()
                wait()
                response = server.by2com(myServer.receive())
                    
                if response == 'y':
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
            myTimer.checkStatus(myServer)
            while(myTimer.running == True):
                myTimer.checkStatus(myServer)
        except Exception as error:
            raise error
         
    
    #PROCESS COMMANDS    
    def process(command):
        try:
            myCommand = command
            command_parts = command.split()
            if myCommand is not None:
                if len(command_parts) < 1:
                    raise RuntimeError(f"Invalid command format")
                
                command_type = command_parts[0]
                if command_type == 'quit':
                    reset()
                    exit
                    
                device = command_parts[1]
                if command_type == 'get':
                    
                    if device == 'printer':
                        if command_parts[2] == 'pos':
                            #Implement logic to get position
                            myData = myPrinter.get_position()
                        elif command_parts[2] == 'speed':
                            #Implement logic to get speed
                            myData = myPrinter.get_speed()
                        elif command_parts[2] == 'temp':
                            #Implement logic to get temperature
                            myData = myPrinter.get_temp()
                        elif command_parts[2] == 'state':
                            #Implement logic to get state
                            myData = myPrinter.get_printer_state()
                        elif command_parts[2] == 'flow':
                            #Implement logic to get flow rate
                            myData = myPrinter.get_flow_rate()
                        else:
                            raise RuntimeError(f"Invalid Printer Command")
                            
                    
                    elif device == 'image':
                    #elif device == 'image':
                        if command_parts[2] == 'cam1':
                            myData = cam1.capture_frame()
                        elif command_parts[2] == 'therm1':
                            myData = therm1.capture_frame()
                        elif command_parts[2] == 'therm2':
                            myData = therm2.capture_frame()
                        else:
                            raise RuntimeError(f"Invalid Image device")
 
                    else:
                        raise RuntimeError(f"Invalid command")
                    
                    if myData is not None:  # Check if image data is not None
                        if myData.type == 'str':
                            myServer.PING()
                            myServer.send(server.com2by(myData))
                            wait()
                        elif myData.type == 'numpy.ndarray':
                            myServer.PING()
                            myServer.send_image(server.im2by(myData))
                            wait()
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
                pass
        except Exception as error:
            raise error
            

    #STOP ALL PROCESSES
    def stop():
        try:
            if myServer.connected:
                myServer.stop_server()
            #if myPrinter.connected:
            #    myPrinter.disconnect()
            #    pass
            if cam1 is not None:
                cam1.release()
            if therm1 is not None:
                therm1.release()
            if therm2 is not None:    
                therm2.release()
        except Exception as error:
            raise error



    """
    DEGUB LOOP
    """
    
    def debug():
        try:    
            while myServer.connected:
                if server.by2com(myServer.receive()) == 'PING':
                    myData = process(server.by2com(myServer.receive())) #PROCESS COMMAND
                    myServer.send('PONG') #SEND PONG (READY TO SEND DATA)
                    myServer.send(server.com2by(myData)) #SEND DATA
        except Exception as error:
            myServer.PONG()
            myServer.send(server.com2by(error))
            myServer.PING()
            raise RuntimeError(f"Error Debugging: {error}")


#MAIN
if __name__ == "__main__":
    try:
        start()
    except Exception as error:
        print(f"Error: {error}")
        """
        try:
            start.myServerPING()
            start.myServer.send(server.com2by('RESET'))
            start.myServer.receive()
            if server.by2com(start.myServer.receive()) == 'QUIT' or server.by2com(start.myServer.receive()) == 'y':
                start.reset()
        except Exception as error:
            raise error   
            print(f"{error}")
        """
        sys.exit(1)