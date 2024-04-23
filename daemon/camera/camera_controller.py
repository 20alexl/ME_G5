#daemon/camera/camera_controller.py
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
        try:
            # Initialize the thermal camera
            self.camera = cv2.VideoCapture(com_port)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
            self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('Y', '1', '6', ' '))
            self.camera.set(cv2.CAP_PROP_CONVERT_RGB, 0)
            if not self.camera.isOpened():
                raise RuntimeError(f"Failed to open camera on COM port {com_port}")
        except Exception as error:
            self.camera = None
            raise RuntimeError(f"Error initializing ThermalCamera: {error}")

    def capture_frame(self):
        """
        Capture a frame from the thermal camera.
        
        Returns:
            np.ndarray: The captured frame as a NumPy array.
        """
        # Capture a frame from the thermal camera
        try:
            if self.camera is not None:
                # Capture a frame from the thermal camera
                ret, frame = self.camera.read()
                return ret, frame
            else:
                return False, None
        except Exception as error:
            raise RuntimeError(f"Error capturing frame from ThermalCamera: {error}")
            return False, None

    def release(self):
        """Release the thermal camera."""
        if self.camera is not None:
            self.camera.release()


class BasicUSBcamera:
    """Represents a basic USB camera for capturing images."""
    
    def __init__(self, com_port):
        """
        Initialize the BasicUSBcamera.
        
        Args:
            com_port (int): The COM port number of the USB camera.
        """
        try:
            # Initialize the basic USB camera
            self.camera = cv2.VideoCapture(com_port)
            if not self.camera.isOpened():
                raise RuntimeError(f"Failed to open camera on COM port {com_port}")
        except Exception as error:
            self.camera = None
            raise RuntimeError(f"Error initializing BasicUSBcamera: {error}")

    def capture_frame(self):
        """
        Capture a frame from the basic USB camera.
        
        Returns:
            np.ndarray: The captured frame as a NumPy array.
        """
        try:
            if self.camera is not None:
                # Capture a frame from the basic USB camera
                ret, frame = self.camera.read()
                return ret, frame
            else:
                return False, None
        except Exception as error:
            raise RuntimeError(f"Error capturing frame from BasicUSBcamera: {error}")
            return False, None

    def release(self):
        """Release the basic USB camera."""
        if self.camera is not None:
            self.camera.release()
