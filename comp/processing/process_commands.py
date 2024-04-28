#comp/processing/process_commands.py

#Set commands for LWOI-AMP to return
class Commands:
    """Class for sending preset commands to the 3D printer."""

    def __init__(self):
        """
        Initialize the Command Information object.
        """

    def get_printer_state(self):
        """
        Get the current state of the printer.
        """
        return ("get printer state")

    def get_print_progress(self):
        """
        Get the progress of the current print job.
        """
        return ("get printer progress")

    def get_temperatures(self):
        """
        Get the temperatures of the bed and extruder(s).
        """
        return ("get printer temp")


    def cancel_print(self):
        """
        Cancel the print job.
        """
        return ("STOP")

    def home(self, axis):
        """
        Home the specified axis.
        Args:
            axis (str): The axis to home (e.g., 'X', 'Y', 'Z').
        """
        return ("set printer home")

    def move_axis(self, axis, distance):
        """
        Move the specified axis by the given distance.
        Args:
            axis (str): The axis to move (e.g., 'X', 'Y', 'Z').
            distance (float): The distance to move the axis.
        """
        return ("set printer axis " + {axis} + " " + {distance})

    def set_bed_temperature(self, temperature):
        """
        Set the temperature of the bed.
        Args:
            temperature (int): The temperature to set for the bed.
        """
        return ("set printer temp bed " + {temperature})

    def set_extruder_temperature(self, temperature):
        """
        Set the temperature of the extruder.
        Args:
            temperature (int): The temperature to set for the extruder.
            tool (int): The tool/extruder number (default is 0).
        """
        return ("set printer temp extruder " + {temperature})

    def get_bed_temperature(self):
        """
        Get the current temperature of the bed.
        """
        return ("get printer temp bed")

    def get_extruder_temperature(self, tool=0):
        """
        Get the current temperature of the specified extruder.
        Args:
            tool (int): The tool/extruder number (default is 0).
        """
        return ("get printer temp extruder")

    def set_flow_rate(self, rate):
        """
        Set the extrusion flow rate.
        Args:
            rate (float): The extrusion flow rate multiplier.
        """
        return ("set printer flowrate " + {rate})

    def get_flow_rate(self):
        """
        Get the current extrusion flow rate.
        """
        return ("get printer flowrate")

    def set_print_speed(self, speed):
        """
        Set the print speed.
        Args:
            speed (int): The print speed in percentage.
        """
        return ("set printer speed " + {speed})

    def get_print_speed(self):
        """
        Get the current print speed.
        """
        return ("get printer speed")

    def get_printer_info(self):
        """
        Get general information about the printer.
        """
        return ("get printer info")

    def get_axis_position(self, axis):
        """
        Get the current position of the specified axis.
        Args:
            axis (str): The axis to retrieve the position of (e.g., 'X', 'Y', 'Z').
        """
        return ("get printer axis " + {axis})
    
    def get_image(self, cam):
        return ("get image ", + {cam})
    
    def layer0(self):
        try:
            cmd = self.get_image("therm1") + '\n' + self.get_temperatures()
            return (cmd)
        except Exception as error:
            pass
