#Main controller for Comp

import threading
import sys

from communication_client.client import CommunicationClient
    
# Global variables
host = "192.168.10.174"
port = 12345

def comp_init():
    """
    Initialize the main controller for the Comp.
    
    Returns:
        CommunicationClient: An instance of the CommunicationClient class.
    """
    client = CommunicationClient(host, port)
    client.connect_to_server()
    return client

def start():
    pass

if __name__ == "__main__":
    client = comp_init()
    while True:
        command = input("Enter command (e.g., 'get image cam1', 'set speed 50', 'quit'): ")
        if command == 'quit':
            break
        client.send_command(command)
    client.close_connection()

  