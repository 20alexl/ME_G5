# Empty file

from . import server
from . import timing
import cv2

def com2by(self, data):
    """
    Convert text data to bytes.

    Args:
        data (str): The text data to be converted.

    Returns:
        bytes: The converted byte data.
    """
    try:
        return data.encode('utf-8')
    except Exception as error:
        raise RuntimeError(f"Error converting text to bytes: {error}")
        return None

def im2by(self, data):
    """
    Convert image data to bytes.

    Args:
        data: The image data to be converted.

    Returns:
        bytes: The converted byte data.
    """
    try:
        return cv2.imencode('.jpg', data)[1].tobytes()
    except Exception as error:
        raise RuntimeError(f"Error converting image to bytes: {error}")
        return None

def by2com(self, data):
    """
    Convert bytes data to text.

    Args:
        data (bytes): The byte data to be converted.

    Returns:
        str: The converted text data.
    """
    try:
        return data.decode('utf-8')
    except Exception as error:
        raise RuntimeError(f"Error converting bytes to text: {error}")
        return None

#Test function
def test(server):
        if server.connected == True:
            try:
                
                status, _ = timing.status()
                if not status:
                    _, data = timing.status()
                    print("Server Test Complete: PING / ", data)
            except Exception as error:
                raise RuntimeError (f"Error Testing Server: {error}")
            
