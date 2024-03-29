# Code for controlling the 3D printer
import serial

class PrinterCommunication:
    """Class for handling communication with the 3D printer."""
    
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
        """
        Initialize the PrinterCommunication object.

        Args:
            port (str): The port to connect to the printer.
            baudrate (int): The baud rate for the serial communication.
        """
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=1)
    
    def send_command(self, command):
        """
        Send a command to the printer.

        Args:
            command (str): The command to send to the printer.
        """
        self.serial_connection.write((command + "\n").encode())
    
    def receive_response(self):
        """
        Receive a response from the printer.

        Returns:
            str: The response received from the printer.
        """
        return self.serial_connection.readline().decode().strip()
    
    def close_connection(self):
        """Close the serial connection to the printer."""
        self.serial_connection.close()


