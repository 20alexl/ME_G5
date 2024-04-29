#daemon/printer/printer_parser.py

# Code for parsing G-code commands
class Commands:
    """Class for sending preset commands to the 3D printer."""

    def __init__(self, communication):
        """
        Initialize the PrinterInformation object.

        Args:
            communication (PrinterCommunication): The communication object for interacting with the printer.
        """
        self.communication = communication

    def get_printer_state(self):
        """
        Get the current state of the printer.
        """
        self.communication.send_command("M27")
        return self.communication.receive_response()

    def get_print_progress(self):
        """
        Get the progress of the current print job.
        """
        self.communication.send_command("M27")
        return self.communication.receive_response()

    def get_temperatures(self):
        """
        Get the temperatures of the bed and extruder(s).
        """
        self.communication.send_command("M105")
        return self.communication.receive_response()

    def start_print(self):
        """
        Start the print job.
        """
        self.communication.send_command("M24")

    def pause_print(self):
        """
        Pause the print job.
        """
        self.communication.send_command("M25")

    def resume_print(self):
        """
        Resume the print job.
        """
        self.communication.send_command("M24")

    def cancel_print(self):
        """
        Cancel the print job.
        """
        self.communication.send_command("M524")

    def home_axis(self, axis):
        """
        Home the specified axis.
        Args:
            axis (str): The axis to home (e.g., 'X', 'Y', 'Z').
        """
        self.communication.send_command("G28 " + axis)

    def home(self, axis):
        """
        Home the specified axis.
        Args:
            axis (str): The axis to home (e.g., 'X', 'Y', 'Z').
        """
        self.communication.send_command("G28 ")
        return self.communication.receive_response()

    def move_axis(self, axis, distance):
        """
        Move the specified axis by the given distance.
        Args:
            axis (str): The axis to move (e.g., 'X', 'Y', 'Z').
            distance (float): The distance to move the axis.
        """
        self.communication.send_command("G1 " + axis + str(distance))
        return self.communication.receive_response()

    def set_bed_temperature(self, temperature):
        """
        Set the temperature of the bed.
        Args:
            temperature (int): The temperature to set for the bed.
        """
        self.communication.send_command("M140 S" + str(temperature))
        return self.communication.receive_response()

    def set_extruder_temperature(self, temperature, tool=0):
        """
        Set the temperature of the extruder.
        Args:
            temperature (int): The temperature to set for the extruder.
            tool (int): The tool/extruder number (default is 0).
        """
        self.communication.send_command("M104 T" + str(tool) + " S" + str(temperature))
        return self.communication.receive_response()

    def set_fan_speed(self, speed):
        """
        Set the fan speed.
        Args:
            speed (int): The speed of the fan (0-255).
        """
        self.communication.send_command("M106 S" + str(speed))
        return self.communication.receive_response()

    def get_bed_temperature(self):
        """
        Get the current temperature of the bed.
        """
        self.communication.send_command("M105")
        return self.communication.receive_response()

    def get_extruder_temperature(self, tool=0):
        """
        Get the current temperature of the specified extruder.
        Args:
            tool (int): The tool/extruder number (default is 0).
        """
        self.communication.send_command("M105 T" + str(tool))
        return self.communication.receive_response()

    def set_flow_rate(self, rate):
        """
        Set the extrusion flow rate.
        Args:
            rate (float): The extrusion flow rate multiplier.
        """
        self.communication.send_command("M221 S" + str(rate))
        return self.communication.receive_response()

    def get_flow_rate(self):
        """
        Get the current extrusion flow rate.
        """
        self.communication.send_command("M221")
        return self.communication.receive_response()

    def set_print_speed(self, speed):
        """
        Set the print speed.
        Args:
            speed (int): The print speed in percentage.
        """
        self.communication.send_command("M220 S" + str(speed))
        return self.communication.receive_response()

    def get_print_speed(self):
        """
        Get the current print speed.
        """
        self.communication.send_command("M220")
        return self.communication.receive_response()

    def get_printer_info(self):
        """
        Get general information about the printer.
        """
        self.communication.send_command("M115")
        return self.communication.receive_response()

    def get_axis_position(self, axis):
        """
        Get the current position of the specified axis.
        Args:
            axis (str): The axis to retrieve the position of (e.g., 'X', 'Y', 'Z').
        """
        self.communication.send_command(f"M114 {axis}")
        return self.communication.receive_response()

    def park(self):
        """
        Pause and park the printer. In halt state
        """
        self.communication.send_command("M125")
        return self.communication.receive_response()

    def clear(self):
        """
        Clear the halt state of the printer.
        """
        self.communication.send_command("M108")
        return self.communication.receive_response()
