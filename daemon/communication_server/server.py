from email.mime import image
import socket
import cv2
import pickle
import struct

class CommunicationServer:
    def __init__(self, host, port, cam1, therm1, therm2, printer):
        self.host = host
        self.port = port
        self.server_socket = None
        self.cam1 = cam1
        self.therm1 = therm1
        self.therm2 = therm2
        self.printer = printer

    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            print(f"Server listening on {self.host}:{self.port}")
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection established with {client_address}")
                self.handle_client(client_socket)
        except Exception as e:
            print(f"Error starting server: {e}")
            
    def stop_server(self):
        if self.server_socket:
            self.server_socket.close()
            print("Server stopped")
            

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                command_parts = data.split()
                if len(command_parts) < 3:
                    client_socket.send(b"Invalid command format")
                    continue
                command_type = command_parts[0]
                device = command_parts[2]
                if command_type == 'quit':
                    self.stop_server()
                    break
                
                elif command_type == 'get':
                    if device == 'image':
                        if command_parts[1] == 'cam_top':
                            image_data = self.cam1.capture_frame()
                        elif command_parts[1] == 'top':
                            image_data = self.therm1.capture_frame()
                        elif command_parts[1] == 'side':
                            image_data = self.therm2.capture_frame()
                        else:
                            client_socket.send(b"Invalid device")
                            continue
                        if image_data:
                            self.send_image(client_socket, image_data)
                        else:
                            client_socket.send(b"Error: Failed to capture image")
                    else:
                        client_socket.send(b"Invalid command")
                        
                elif command_type == 'set':
                    if device == 'speed':
                        # Implement logic to set speed
                        client_socket.send(b"Speed set successfully")
                    elif device == 'temp':
                        # Implement logic to set temperature
                        client_socket.send(b"Temperature set successfully")
                    else:
                        client_socket.send(b"Invalid device")
                        
                else:
                    client_socket.send(b"Invalid command")
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def capture_image(self, camera):
        # Capture an image using the specified camera
        return camera.capture_frame()

    def send_image(self, client_socket, image_data):
        # Send image data over the socket
        try:
            data = pickle.dumps(image_data)
            client_socket.sendall(struct.pack("L", len(data)) + data)
        except Exception as e:
            print(f"Error sending image: {e}")


if __name__ == "__main__":
    # Assuming you have camera objects cam1, therm1, therm2, and a printer object printer
    server = CommunicationServer('localhost', 8888, cam1, therm1, therm2, printer)
    server.start_server()
