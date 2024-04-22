#daemon/printer/printer_controller.py

# Code for controlling the 3D printer
import serial
import printer_commands as commands

class PrinterCommunication():
    """Class for handling communication with the 3D printer."""

    def __init__(self, port='/dev/ttyUSB0', baudrate=250000):
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
        self.setCommands = commands.Commands(self)
        self.connect()

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
        self.cmd = self.serial_connection.readline().decode().strip()
        if not self.printing:
            self.parse()
            if self.cmd_split[0] == "FILE":
                self.printing = True
        return self.cmd

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
            if self.printing:
                self.cmd_split = self.cmd.split(':')
                self.cmd_split[0].strip(';')
                #REMOVE THE ; AND SPLIT BY : (LAYER, __)
            else:
                self.cmd_split = self.cmd.split(':')
                self.cmd_split.append = self.cmd.split() #?
                self.cmd_split[0].strip('//')
                self.cmd_split[0].strip(';')
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
        self.parse()

        #If we are not printing, return the status
        if not self.printing:  
            return None

        #Return status
        if not self.init: #CHECK FOR START #GET INIT STATES
            if self.cmd_split[0] == "TARGET_MACHINE.NAME":
                self.init = True
                return {"INIT" + self.initState}
            else:
                self.initState = self.initState + " " + self.cmd
                return None

        else: #IF we have started a print
            if self.cmd_split[0] == "LAYER": #LAYER FLAG
                return {"LAYER " + self.cmd_split[1]}
            #elif self.cmd_split[0] == "TIME": #TIME FLAG
                return {"TIME " + self.cmd_split[1]}
            else:
                return None


if __name__ == "__main__":
    """
    MAIN INITIALIZATION
    """

    printer = PrinterCommunication('COM6', 115200)

    while (True):
        com = input("Press Enter! or enter command")
        if com:
            printer.send_command(com)
        else:
            #printer.send_command("M105")
            printer.setCommands.get_temperatures()
            pass
        response = printer.receive_response()
        print(response)