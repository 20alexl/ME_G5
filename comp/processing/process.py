#comp/processing/process.py

# Code for controlling the image processing
import cv2
import numpy as np


class ImageProcess:
    def __init__(self):
        self.image = None
        self.printerFlag = str(None)
        self.runnning = bool(True)

        self.DArray = None

        self.layer = int(0)
        self.layerHeight = int(None)
        self.layerMax = int(None)

        self.minX = int(None)
        self.minY = int(None)
        self.minZ = int(None)
        self.maxX = int(None)
        self.maxY = int(None)
        self.maxZ = int(None)
        self.E = int(None)
        self.Temp = int(None) 
        self.Bed = int(None)

        self.CalTemp = int(None)
        self.CalBed = int(None)


    def calibrate_data(self, init):
        try:
            init = init.split()
            for l in range(len(init)):
                split = init[l].split(':')
                if split[0] == 'Filament used':
                    self.E = int(split[1])
                if split[0] == 'Layer height':
                    self.layerHeight = int(split[1])
                if split[0] == 'MINX':
                    self.minX = int(split[1])
                if split[0] == 'MINY':
                    self.minY = int(split[1])
                if split[0] == 'MINZ':
                    self.minZ = int(split[1])
                if split[0] == 'MAXX':
                    self.maxX = int(split[1])
                if split[0] == 'MAXY':
                    self.maxY = int(split[1])
                if split[0] == 'MAXZ':
                    self.maxZ = int(split[1])

        except Exception as error:
            raise RuntimeError(f"Error calibrate_data: {error}")
        #READ INIT


    def layer_change(self, layer):
        try:
            self.layer = layer
        except Exception as error:
            raise RuntimeError(f"Error layer_change: {error}")
        #READ LAYER CHANGE


    def LWOI_AMP(self, image):
        try:
            pass
        except Exception as error:
            raise RuntimeError(f"Error LWOI_AMP: {error}")
        #LAYER-WISE-OPTICAL-INSPECTION of ADDITIVELY-MANUFACTURED-PARTS
        #READ TEMP DATA
        #COMPARE TO CALIBRATION DATA
        #COMPARE MODEL TEMP TO BED TEMP
        #SET BED TEMP TO MODEL TEMP OR NEAR TO ALLOW MORE EVEN COOLING


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