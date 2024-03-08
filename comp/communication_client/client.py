import socket
import sys
import threading

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        print(f"Connecting to {self.host}:{self.port}...")
        self.socket.connect((self.host, self.port))
        print("Connected to server")
        
    def send_data(self):
        while True:
            data = input("Enter data to send (or 'q' to quit): ")
            if data == 'q':
                break
            self.socket.sendall(data.encode('utf-8'))
        
    def receive_data(self):
        while True:
            data = self.socket.recv(1024)
            if not data:
                break
            print(f"Received data from server: {data.decode('utf-8')}")
        
    def disconnect(self):
        print("Disconnecting from server...")
        self.socket.close()

    def stop(self):
        print("Quitting...")
        self.socket.close()
        sys.exit()

if __name__ == "__main__":
    host = "192.168.10.174"  # Raspberry Pi IP address
    port = 12345  # Chosen port number
    client = Client(host, port)
    client.connect()

    client = Client(host, port)
    client.connect()

    # Start a separate thread to continuously receive adn send data from the server
    send_thread = threading.Thread(target=client.send_data)
    send_thread.start()

    receive_thread = threading.Thread(target=client.receive_data)
    receive_thread.start()
