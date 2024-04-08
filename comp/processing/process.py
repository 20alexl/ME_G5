#comp/processing/process.py

# Code for controlling the image processing
import cv2
import numpy as np


class ImageProcess:
    def __init__(self):
        self.image = None
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

    
    def display_image(self, image):
        try:
            self.image = image
            if self.image is not None:
                cv2.imshow("Image", self.image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                raise RuntimeError("No image to display")
        except Exception as error:
            raise RuntimeError(f"Error displaying image: {error}")
        #READ TEMP DATA
        #COMPARE TO CALIBRATION DATA
        #COMPARE MODEL TEMP TO BED TEMP
        #SET BED TEMP TO MODEL TEMP OR NEAR TO ALLOW MORE EVEN COOLING