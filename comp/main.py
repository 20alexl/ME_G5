import threading
import sys

from communication_client.client import Client as C
    
def clientInit(h, p):
    
    client = C(h, p)
    client.connect()
    
    # Start a separate thread to continuously receive adn send data from the server
    send_thread = threading.Thread(target=client.send_data)
    send_thread.start()

    receive_thread = threading.Thread(target=client.receive_data)
    receive_thread.start()
    return client

if __name__ == "__main__":
    host = "192.168.10.174"  # Raspberry Pi IP address
    port = 12345  # Chosen port number

    client = clientInit(host, port)
    