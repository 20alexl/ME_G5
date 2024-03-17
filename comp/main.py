import threading
import sys

from communication_client.client import CommunicationClient
    
#global variables
host = "192.168.10.174"
port = 12345

def comp_init():
    
    client = CommunicationClient(host, port)
    client.connect_to_server()
    return client

def start():
    pass
    

if __name__ == "__main__":
    client = comp_init(host, port)
    while True:
        command = input("Enter command (e.g., 'get image cam1', 'set speed 50', 'quit'): ")
        if command == 'quit':
            break
        client.send_command(command)
    client.close_connection()
    