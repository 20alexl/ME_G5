# Empty file

from . import camera_controller

def test(cam):
    """
    Test if the camera is able to capture a frame.

    Args:
        cam: An instance of a camera object (ThermalCamera or BasicUSBcamera).

    Returns:
        bool: True if the camera captures a frame successfully, False otherwise.
    """
    try:
        if cam.camera is not None:
            ret, frame = cam.capture_frame()
            if ret:
                return True
            else:
                raise RuntimeError(f"Error testing camera: No Frame")
                return False
        else:
            raise RuntimeError(f"Error testing camera: No Camera Object")
            return False
    except Exception as error:
        raise RuntimeError(f"Error testing camera: {error}")
        return False