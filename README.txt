HELP

# ME_G5 Python Package

This package contains code for communication between a Raspberry Pi (daemon) and an external computer (comp).

## Raspberry Pi (daemon)

### Camera
- `camera_controller.py`: Code for controlling the camera on the Raspberry Pi.
- `video_streaming.py`: Code for live video streaming from the camera.

### Printer
- `printer_controller.py`: Code for controlling the 3D printer.
- `gcode_parser.py`: Code for parsing G-code commands.

### Communication Server
- `server.py`: Code for communication server on the Raspberry Pi.
- `client.py`: Code for communication client on the Raspberry Pi.

## External Computer (comp)

### Communication Client
- `client.py`: Code for communication client on the external computer.
