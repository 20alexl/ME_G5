import socket
import numpy as np
import struct
import cv2
import threading

class CommunicationClient:
    """A TCP client for communicating with the server."""
    
    def __init__(self, host, port):
        """
        Initialize the CommunicationClient.
        
        Args:
            host (str): The IP address of the server.
            port (int): The port number to connect to.
        """
        self.host = host
        self.port = port
        self.client_socket = None

    def connect_to_server(self):
        """
        Connect to the server.
        """
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
        except Exception as e:
            print(f"Error connecting to server: {e}")
            
        
    def send_command(self, command):
        """
        Send a command to the server and process the response.
        
        Args:
            command (str): The command to send to the server.
        """
        try:
            self.client_socket.sendall(command.encode())
            if command.startswith('get image'):
                length_data = self.client_socket.recv(4)
                length = int.from_bytes(length_data, 'big')
                data = b''
            
                while len(data) < length:
                    data += self.client_socket.recv(length - len(data))
                self.process_response(data, length)
            else:
                data = self.client_socket.recv(1024)
                self.process_response(data, 1)
        except Exception as e:
            print(f"Error sending command: {e}")

    def process_response(self, data, byte_length):
        """
        Process the response received from the server.
        
        Args:
            data: The data received from the server.
            byte_length (int): The length of the data received.
        """
        try:
            if byte_length > 1:
                self.display_image(data)
            else:
                print(data.decode('utf-8'))
        except Exception as e:
            print(f"Error processing response: {e}")


    def display_image(self, image_data):
        """
        Display the received image.
        
        Args:
            image_data: The image data received from the server.
        """
        try:
            print(f"Received image data length: {len(image_data)}")
            # Decode the image data and reshape it into the original image dimensions
            #frame = np.frombuffer(image_data, dtype=np.uint8).reshape((360, 640, 3))
            frame = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
        
            # Check if the frame is None or empty
            if frame is None or len(frame) == 0:
                print("Error: Received empty or invalid image data")
                return
        
            # Display the image
            cv2.imshow("Image", frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except Exception as e:
            print(f"Error displaying image: {e}")

    def close_connection(self):
        """Close the connection with the server."""
        if self.client_socket:
            self.send_command('quit')
            self.client_socket.close()
            print("Connection closed")
            
    def errorHandle(self, e):
        pass

if __name__ == "__main__":
    client = CommunicationClient('localhost', 8888)
    client.connect_to_server()
    while True:
        command = input("Enter command (e.g., 'get image cam1', 'set speed 50', 'quit'): ")
        if command == 'quit':
            break
        client.send_command(command)
    client.close_connection()
