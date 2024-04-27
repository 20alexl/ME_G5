#comp/communication_client/__init__.py
from . import client
import cv2
import numpy as np


def com2by(data):
    """
    Convert text data to bytes.

    Args:
        data (str): The text data to be converted.

    Returns:
        bytes: The converted byte data.
    """
    try:
        if data is None:
            return None
        else:
            data = data.encode()
            return data
    except Exception as error:
        raise RuntimeError(f"Error converting text to bytes: {error}")
        return None

def im2by(data):
    """
    Convert image data to bytes.

    Args:
        data: The image data to be converted.

    Returns:
        bytes: The converted byte data.
    """
    try:
        if data is None:
            return None
        else:
            return cv2.imencode('.jpg', data)[1].tobytes()
    except Exception as error:
        raise RuntimeError(f"Error converting image to bytes: {error}")
        return None

def by2com(data):
    """
    Convert bytes data to text.

    Args:
        data (bytes): The byte data to be converted.

    Returns:
        str: The converted text data.
    """
    try:
        if data is None:
            return None
        else:
            data =  data.decode()
            return data
    except Exception as error:
        raise RuntimeError(f"Error converting bytes to text: {error}")
        return None
    
def by2im(data, type):
    """
    Convert bytes data to image.

    Args:
        data (bytes): The byte data to be converted.

    Returns:
        str: The converted image data.
    """
    try:
        if data is None:
            return None
        else:
            if type == "therm1" or type == "therm2":
                data = cv2.imdecode(np.frombuffer(data, np.uint16), cv2.IMREAD_UNCHANGED)
                return data
            else:
                data = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
                return data
    except Exception as error:
        raise RuntimeError(f"Error converting bytes to text: {error}")
        return None

#Test function (NOT USED)
"""    
def test(client, timer):
        if client.connected == True:
            try:
                counter = 0
                timer.checkStatus(client)
                while(timer.running == True and counter < 20):
                    timer.checkStatus(client)
                    counter += 1
                if counter == 20:
                    raise RuntimeError (f"Error Testing Server: TIMEOUT 20+")
                else:
                    client.PONG()
            except Exception as error:
                raise RuntimeError (f"Error Testing Server: {error}")
"""    