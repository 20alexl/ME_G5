#daemon/printer/printer_controller.py

# Code for controlling the 3D printer
import serial
from . import printer_commands as commands

class PrinterCommunication():
    """Class for handling communication with the 3D printer."""

    def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
        """
        Initialize the PrinterCommunication object.
        Args:
            port (str): The port to connect to the printer.
            baudrate (int): The baud rate for the serial communication.
        """
        self.serial_connection = None
        self.init = False
        self.initState = ""
        self.cmd = None
        self.cmd_split = None

        self.port = port
        self.baudrate = baudrate
        self.connected = False
        self.printing = False
        self.paused = False
        self.gcodeTail = "\r\n"
        self.connect()
        self.setCommands = commands.Commands(self)

    def connect(self):
        """
        Connect to the printer.
        """
        print("Connecting to printer...")
        self.serial_connection = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=1)
        self.connected = True

    def send_command(self, commands):
        """
        Send a command to the printer.
        Args:
            command (str): The command to send to the printer.
        """
        if isinstance(commands, str):
            commands = [commands]  # Convert single command to a list
        for self.cmd in commands:
            self.serial_connection.write((self.cmd + self.gcodeTail).encode())
            #self.receive_response()

    def receive_response(self):
        """
        Receive a response from the printer.
        Returns:
            str: The response received from the printer.
        """
        self.cmd = self.serial_connection.readline().decode()
        #print(self.cmd)
        self.parse()
        if self.cmd_split[0] == 'busy' or self.cmd_split[0] == '':
            return True
        if self.cmd_split[0] == 'FLAVOR':
            self.printing = True

        return False

    def close_connection(self):
        """Close the serial connection to the printer."""
        self.serial_connection.close()

    def pause(self):
        """Pause the printer."""
        self.setCommands.park()
        self.paused = True

    def resume(self):
        """Resume the printer."""
        self.setCommands.resume()
        self.paused = False

    def parse(self):
        """Parse the response"""
        if self.cmd is not None:
            try:
                self.cmd = self.cmd.strip()
                self.cmd = self.cmd.strip('\r\n')
                self.cmd = self.cmd.strip(';')
                self.cmd = self.cmd.strip('//echo:')
                self.cmd = self.cmd.strip('ok ')
                self.cmd_split = self.cmd.split(':')

            except:
                pass
                #REMOVE THE ; AND SPLIT BY : (LAYER, __)
                #REMOVE THE // AND SPLIT BY : (ACTION, __) or (FILE, ___)

    def get_status(self):
        """
        Get the status of the printer.
        Returns:
            dict: The status of the printer.
        """

        #Get response from printer
        self.receive_response()
        #Parse response
        print(self.cmd_split)

        #If we are not printing, return the status
        if self.printing == False:  
            return None

        #Return status
        if not self.init: #CHECK FOR START #GET INIT STATES
            if self.cmd_split[0] == 'LAYER_COUNT':
                self.initState = self.initState + " " + (self.cmd).strip(";")
                self.init = True
                return ("INIT" + str(self.initState))
            else:
                self.initState = self.initState + " " + (self.cmd).strip(";")
                return None

        else: #IF we have started a print
            if self.cmd_split[0] == 'LAYER': #LAYER FLAG
                return ("LAYER " + self.cmd_split[1])
            #elif self.cmd_split[0] == "TIME": #TIME FLAG
                return {"TIME " + self.cmd_split[1]}
            else:
                return None


if __name__ == "__main__":
    """
    MAIN INITIALIZATION
    """

    printer = PrinterCommunication('COM4', 115200)

    while (True):
        cmd = printer.get_status()
        if cmd is not None:
            print(cmd)