# Code for communication server on the Raspberry Pi
import socket
import sys
import threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        print("Starting communication server...")
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            client_socket, client_address = self.socket.accept()
            print(f"Connection from {client_address}")
            # Start a new thread to handle client communication
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        receive_thread = threading.Thread(target=self.receive_data, args=(client_socket,))
        receive_thread.start()

        while True:
            try:
                data = input("Enter data to send (or 'q' to quit): ")
                if data == 'q':
                    break
                client_socket.sendall(data.encode('utf-8'))
            except BrokenPipeError:
                print("Client disconnected unexpectedly")
                break

        client_socket.close()
        
    def receive_data(self, client_socket):
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received data from client: {data.decode('utf-8')}")

if __name__ == "__main__":
    host = "192.168.10.174"  # Raspberry Pi IP address
    port = 12345  # Chosen port number
    server = Server(host, port)
    server.start()