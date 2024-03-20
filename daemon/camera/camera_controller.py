import cv2

class ThermalCamera:
    """Represents a thermal camera for capturing thermal images."""
    
    def __init__(self, com_port):
        """
        Initialize the ThermalCamera.
        
        Args:
            com_port (int): The COM port number of the thermal camera.
        """
        # Initialize the thermal camera
        self.camera = cv2.VideoCapture(com_port, cv2.CAP_DSHOW)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
        self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('Y', '1', '6', ' '))
        self.camera.set(cv2.CAP_PROP_CONVERT_RGB, 0)

    def capture_frame(self):
        """
        Capture a frame from the thermal camera.
        
        Returns:
            np.ndarray: The captured frame as a NumPy array.
        """
        # Capture a frame from the thermal camera
        ret, frame = self.camera.read()
        if ret:
            return frame
        else:
            print("Error: Failed to capture frame from the thermal camera.")
            return None

    def release(self):
        """Release the thermal camera."""
        self.camera.release()


class BasicUSBcamera:
    """Represents a basic USB camera for capturing images."""
    
    def __init__(self, com_port):
        """
        Initialize the BasicUSBcamera.
        
        Args:
            com_port (int): The COM port number of the USB camera.
        """
        # Initialize the basic USB camera
        self.camera = cv2.VideoCapture(com_port)
        if not self.camera.isOpened():
            print(f"Error: Failed to open camera on COM port {com_port}")
            return
        
        # Additional setup for camera if needed
        # For example, setting camera parameters

    def capture_frame(self):
        """
        Capture a frame from the basic USB camera.
        
        Returns:
            np.ndarray: The captured frame as a NumPy array.
        """
        # Capture a frame from the basic USB camera
        ret, frame = self.camera.read()
        if ret:
            return frame
        else:
            print("Error: Failed to capture frame from the basic USB camera.")
            return None

    def release(self):
        """Release the basic USB camera."""
        self.camera.release()
