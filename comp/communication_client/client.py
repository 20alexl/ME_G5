import socket
import pickle
import struct
import cv2

class CommunicationClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def send_command(self, command):
        try:
            self.client_socket.sendall(command.encode())
            data = self.client_socket.recv(1024)
            self.process_response(data)
        except Exception as e:
            print(f"Error sending command: {e}")

    def process_response(self, data):
        if data.startswith(b"\x89PNG"):
            self.display_image(data)
        else:
            print(data.decode())

    def display_image(self, image_data):
        try:
            image_size = struct.unpack("L", image_data[:struct.calcsize("L")])[0]
            image_data = image_data[struct.calcsize("L"):]
            if len(image_data) != image_size:
                print("Error: Image data corrupted")
                return
            image = pickle.loads(image_data)
            cv2.imshow("Image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except Exception as e:
            print(f"Error displaying image: {e}")
            
    def return_image(self, image_data):
        try:
            image_size = struct.unpack("L", image_data[:struct.calcsize("L")])[0]
            image_data = image_data[struct.calcsize("L"):]
            if len(image_data) != image_size:
                print("Error: Image data corrupted")
                return
            else:
                image = pickle.loads(image_data)
                return image
        except Exception as e:
            print(f"Error returning image: {e}")

    def close_connection(self):
        if self.client_socket:
            self.client_socket.close()
            print("Connection closed")

if __name__ == "__main__":
    client = CommunicationClient('localhost', 8888)
    client.connect_to_server()
    while True:
        command = input("Enter command (e.g., 'get image cam1', 'set speed 50', 'quit'): ")
        if command == 'quit':
            break
        client.send_command(command)
    client.close_connection()
