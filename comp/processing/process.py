# Code for controlling the image process

import cv2
import numpy as np


class ImageProcess:
    def __init__(self, frame):
        self.image = frame
        self.printerFlag = None
        self.runnning = True
        
        self.DArray = None
        
        self.X = None
        self.Y = None
        self.Z = None
        self.E = None
        self.Temp = None
        self.Bed = None
        
        self.CalTemp = None
        self.CalBed = None


    def display_image(self):
        try:
            if self.image is not None:
                cv2.imshow("Image", self.image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                raise RuntimeError("No image to display")
        except Exception as error:
            raise RuntimeError(f"Error displaying image: {error}")
        