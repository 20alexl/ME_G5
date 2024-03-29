# Code for parsing G-code commands
class PrinterInformation:
    """Class for retrieving information from the 3D printer."""
    
    def __init__(self, communication):
        """
        Initialize the PrinterInformation object.

        Args:
            communication (PrinterCommunication): The communication object for interacting with the printer.
        """
        self.communication = communication
    
    def parse_response(self, response):
        """
        Parse the response received from the printer.

        Args:
            response (str): The response received from the printer.

        Returns:
            str: Parsed information from the response.
        """
        # Very basic parser, you may need to adjust according to your printer's responses
        return response.split(":")[-1].strip()
    
    def get_printer_state(self):
        """
        Get the current state of the printer.

        Returns:
            str: The current state of the printer.
        """
        self.communication.send_command("M27")
        response = self.communication.receive_response()
        return self.parse_response(response)
    
    def get_print_progress(self):
        """
        Get the progress of the current print job.

        Returns:
            str: The progress of the current print job.
        """
        self.communication.send_command("M27")
        response = self.communication.receive_response()
        return self.parse_response(response)
    
    def get_temperatures(self):
        """
        Get the temperatures of the bed and extruder(s).

        Returns:
            str: The temperatures of the bed and extruder(s).
        """
        self.communication.send_command("M105")
        response = self.communication.receive_response()
        return self.parse_response(response)
    
    def get_sd_files(self):
        """
        Get a list of files on the SD card.

        Returns:
            str: A list of files on the SD card.
        """
        self.communication.send_command("M20")
        response = self.communication.receive_response()
        return self.parse_response(response)
    
    def select_sd_file(self, file_name):
        """
        Select a file from the SD card for printing.

        Args:
            file_name (str): The name of the file to select.

        Returns:
            str: Response indicating success or failure.
        """
        self.communication.send_command("M23 " + file_name)
        response = self.communication.receive_response()
        return self.parse_response(response)
    
    def start_print(self):
        """
        Start the print job.

        Returns:
            str: Response indicating success or failure.
        """
        self.communication.send_command("M24")
        response = self.communication.receive_response()
        return self.parse_response(response)
    
    def pause_print(self):
        """
        Pause the print job.

        Returns:
            str: Response indicating success or failure.
        """
        self.communication.send_command("M25")
        response = self.communication.receive_response()
        return self.parse_response(response)
    
    def resume_print(self):
        """
        Resume the print job.

        Returns:
            str: Response indicating success or failure.
        """
        self.communication.send_command("M24")
        response = self.communication.receive_response()
        return self.parse_response(response)
    
    def cancel_print(self):
        """
        Cancel the print job.

        Returns:
            str: Response indicating success or failure.
        """
        self.communication.send_command("M524")
        response = self.communication.receive_response()
        return self.parse_response(response)
    
    def home_axis(self, axis):
        """
        Home the specified axis.

        Args:
            axis (str): The axis to home (e.g., 'X', 'Y', 'Z').

        Returns:
            str: Response indicating success or failure.
        """
        self.communication.send_command("G28 " + axis)
        response = self.communication.receive_response()
        return self.parse_response(response)
    
    def move_axis(self, axis, distance):
        """
        Move the specified axis by the given distance.

        Args:
            axis (str): The axis to move (e.g., 'X', 'Y', 'Z').
            distance (float): The distance to move the axis.

        Returns:
            str: Response indicating success or failure.
        """
        self.communication.send_command("G1 " + axis + str(distance))
        response = self.communication.receive_response()
        return self.parse_response(response)
    
    def set_bed_temperature(self, temperature):
        """
        Set the temperature of the bed.

        Args:
            temperature (int): The temperature to set for the bed.

        Returns:
            str: Response indicating success or failure.
        """
        self.communication.send_command("M140 S" + str(temperature))
        response = self.communication.receive_response()
        return self.parse_response(response)
    
    def set_extruder_temperature(self, temperature, tool=0):
        """
        Set the temperature of the extruder.

        Args:
            temperature (int): The temperature to set for the extruder.
            tool (int): The tool/extruder number (default is 0).

        Returns:
            str: Response indicating success or failure.
        """
        self.communication.send_command("M104 T" + str(tool) + " S" + str(temperature))
        response = self.communication.receive_response()
        return self.parse_response(response)
    
    def set_fan_speed(self, speed):
        """
        Set the fan speed.

        Args:
            speed (int): The speed of the fan (0-255).

        Returns:
            str: Response indicating success or failure.
        """
        self.communication.send_command("M106 S" + str(speed))
        response = self.communication.receive_response()
        return self.parse_response(response)
    
    def get_fan_speed(self):
        """
        Get the current fan speed.

        Returns:
            str: The current fan speed.
        """
        self.communication.send_command("M106")
        response = self.communication.receive_response()
        return self.parse_response(response)
    
    def get_bed_temperature(self):
        """
        Get the current temperature of the bed.

        Returns:
            str: The current temperature of the bed.
        """
        self.communication.send_command("M105")
        response = self.communication.receive_response()
        return self.parse_response(response)
    
    def get_extruder_temperature(self, tool=0):
        """
        Get the current temperature of the specified extruder.

        Args:
            tool (int): The tool/extruder number (default is 0).

        Returns:
            str: The current temperature of the specified extruder.
        """
        self.communication.send_command("M105 T" + str(tool))
        response = self.communication.receive_response()
        return self.parse_response(response)

    def set_flow_rate(self, rate):
        """
        Set the extrusion flow rate.

        Args:
            rate (float): The extrusion flow rate multiplier.

        Returns:
            str: Response indicating success or failure.
        """
        self.communication.send_command("M221 S" + str(rate))
        response = self.communication.receive_response()
        return self.parse_response(response)

    def get_flow_rate(self):
        """
        Get the current extrusion flow rate.

        Returns:
            str: The current extrusion flow rate.
        """
        self.communication.send_command("M221")
        response = self.communication.receive_response()
        return self.parse_response(response)

    def set_print_speed(self, speed):
        """
        Set the print speed.

        Args:
            speed (int): The print speed in percentage.

        Returns:
            str: Response indicating success or failure.
        """
        self.communication.send_command("M220 S" + str(speed))
        response = self.communication.receive_response()
        return self.parse_response(response)

    def get_print_speed(self):
        """
        Get the current print speed.

        Returns:
            str: The current print speed.
        """
        self.communication.send_command("M220")
        response = self.communication.receive_response()
        return self.parse_response(response)

    def set_extruder_offset(self, offset, tool=0):
        """
        Set the offset for the specified extruder.

        Args:
            offset (float): The offset value.
            tool (int): The tool/extruder number (default is 0).

        Returns:
            str: Response indicating success or failure.
        """
        self.communication.send_command("M218 T" + str(tool) + " S" + str(offset))
        response = self.communication.receive_response()
        return self.parse_response(response)

    def get_extruder_offset(self, tool=0):
        """
        Get the offset for the specified extruder.

        Args:
            tool (int): The tool/extruder number (default is 0).

        Returns:
            str: The offset for the specified extruder.
        """
        self.communication.send_command("M218 T" + str(tool))
        response = self.communication.receive_response()
        return self.parse_response(response)

    def set_bed_leveling(self, level):
        """
        Set the bed leveling.

        Args:
            level (str): The bed leveling settings.

        Returns:
            str: Response indicating success or failure.
        """
        self.communication.send_command("G29 " + level)
        response = self.communication.receive_response()
        return self.parse_response(response)

    def get_bed_leveling(self):
        """
        Get the current bed leveling settings.

        Returns:
            str: The current bed leveling settings.
        """
        self.communication.send_command("G29")
        response = self.communication.receive_response()
        return self.parse_response(response)

    def start_preheat(self, bed_temperature, extruder_temperature, tool=0):
        """
        Start preheating the bed and extruder(s) to the specified temperatures.

        Args:
            bed_temperature (int): The temperature to preheat the bed to.
            extruder_temperature (int): The temperature to preheat the extruder(s) to.
            tool (int): The tool/extruder number (default is 0).

        Returns:
            str: Response indicating success or failure.
        """
        command = "M104 T" + str(tool) + " S" + str(extruder_temperature) + " ; " + \
                  "M140 S" + str(bed_temperature) + " ; " + \
                  "M109 T" + str(tool) + " S" + str(extruder_temperature) + " ; " + \
                  "M190 S" + str(bed_temperature)
        self.communication.send_command(command)
        response = self.communication.receive_response()
        return self.parse_response(response)

    def stop_preheat(self, tool=0):
        """
        Stop preheating the extruder(s) and bed.

        Args:
            tool (int): The tool/extruder number (default is 0).

        Returns:
            str: Response indicating success or failure.
        """
        command = "M104 T" + str(tool) + " S0 ; M140 S0 ; M109 T" + str(tool) + " S0 ; M190 S0"
        self.communication.send_command(command)
        response = self.communication.receive_response()
        return self.parse_response(response)

    def get_printer_info(self):
        """
        Get general information about the printer.

        Returns:
            str: General information about the printer.
        """
        self.communication.send_command("M115")
        response = self.communication.receive_response()
        return self.parse_response(response)
    
    def get_axis_position(self, axis):
        """
        Get the current position of the specified axis.

        Args:
            axis (str): The axis to retrieve the position of (e.g., 'X', 'Y', 'Z').

        Returns:
            str: The current position of the specified axis.
        """
        self.communication.send_command(f"M114 {axis}")
        response = self.communication.receive_response()
        return self.parse_response(response)
    
