#/daemon/communication_server/__init__.py

import time
from . import server
import cv2
import socket

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
            data =  data.encode()
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
            if data.ndim == 2:
                _, encoded_image = cv2.imencode('.png', data, [cv2.IMWRITE_PNG_BILEVEL, 0])
            else:
                _, encoded_image = cv2.imencode('.png', data)
            return encoded_image.tobytes()
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
            data = data.decode()
            return data
    except Exception as error:
        raise RuntimeError(f"Error converting bytes to text: {error}")
        return None

#Test function (NOT USED)
"""    
def test(server, timer):
        if server.connected == True:
            try:
                counter = 0
                server.PING()
                print("PINGGED")
                timer.checkStatus(server)
                print("1 check")
                while(timer.running == True and counter < 20):
                    timer.checkStatus(server)
                    counter += 1
                    print("1 check")
                if counter == 20:
                     raise RuntimeError (f"Error Testing Server: TIMEOUT 20+")
                print("Test Complete")
            except Exception as error:
                raise RuntimeError (f"Error Testing Server: {error}")
"""            
