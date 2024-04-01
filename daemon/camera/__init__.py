# Empty file

from . import camera_controller

OK = False
Errors = []

def setup(names, ports):
    camera = []
    camStatus = [False] * len(names)
    
    for index, string in enumerate(names):
        if string == 'cam1':
            try:
                camera.append(camera_controller.BasicUSBcamera(ports[index]))
                camStatus[index] = True
            except Exception as e:
                print(e)
                Errors[index] = e
                
        elif string == 'therm1' or string == 'therm2':
            try:
                camera.append(camera_controller.ThermalCamera(ports[index]))
                camStatus[index] = True
            except Exception as e:
                print(e)
                Errors[index] = e
        else:
            pass
        
    for index, cam in enumerate(camera):
        print(cam)
        ret, frame = cam.capture_frame()
        if ret:
            camStatus[index] = True
        else:
            camStatus[index] = False
            Errors[index] = "Error: Failed to capture frame from {cam}."
 
    return camera, camStatus