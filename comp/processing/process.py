#comp/processing/process.py

# Code for controlling the image processing
import cv2
import numpy as np

from . import process_commands as commands

class ImageProcess:
    def __init__(self):
        self.image = None
        self.printerFlag = str
        self.runnning = bool(True)

        self.DArray = []
        self.mod = None

        self.layer = int(0)
        self.layerHeight = int
        self.layerMax = int

        self.minX = int
        self.minY = int
        self.minZ = int
        self.maxX = int
        self.maxY = int
        self.maxZ = int
        self.E = int
        self.Temp = int
        self.Bed = int

        self.CalTemp = int
        self.CalBed = int
        
        self.setCommands = commands.Commands()


    def calibrate_data(self, init):
        try:
            #init = init.strip('INIT ')
            init = init.split()
            for l in range(len(init)):
                init_split = init[l].split(':')
                init_split[0] = init_split[0].strip()
                print(init_split)
                if init_split[0] == 'used':
                    init[l+1] = init[l+1].strip()
                    init_split[1] = init[l+1].strip('m')
                    self.E = ((init_split[1]))
                    print("set")
                if init_split[0] == 'height':
                    init_split[1] = init[l+1].strip()
                    self.layerHeight = (init_split[1])
                    print("set")
                if init_split[0] == 'MINX':
                    self.minX = (init_split[1])
                    print("set")
                if init_split[0] == 'MINY':
                    self.minY = (init_split[1])
                    print("set")
                if init_split[0] == 'MINZ':
                    self.minZ = (init_split[1])
                if init_split[0] == 'MAXX':
                    self.maxX = (init_split[1])
                if init_split[0] == 'MAXY':
                    self.maxY = (init_split[1])
                if init_split[0] == 'MAXZ':
                    self.maxZ = (init_split[1])
                if init_split[0] == 'LAYER_COUNT':
                    self.layerMax = (init_split[1])

        except Exception as error:
            raise RuntimeError(f"Error calibrate_data: {error}")
        #READ INIT


    def layer_change(self, layer):
        try:
            self.layer = layer
            if self.layer == 0:
                return self.setCommands.get_calibration_temp()
            else:
                return self.setCommands.get_image_therm1()
        except Exception as error:
            raise RuntimeError(f"Error layer_change: {error}")
        #READ LAYER CHANGE

    def canny(self):
        try:
            self.mod = self.DArray[self.layer].copy()
            edges = cv2.Canny(self.mod, 100, 255)
            indices = np.where(edges != [0])
            coordinates = zip(indices[0], indices[1])
            return coordinates
        except Exception as error:
            pass

    def findBed(self):
        try:
            self.mod = self.DArray[self.layer].copy()
            plate = self.canny()
        except Exception as error:
            pass

    def LWOI_AMP(self, image, flag, calib=None):
        try:
            if self.layer == 0:
                self.CalBed = calib[0] #BED TEMP
                self.CalNozzle = calib[1] #NOZZLE TEMP
            self.DArray[self.layer] = image.copy()
            self.findBed()


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
        

if __name__ == "__main__":
    process = ImageProcess()
    
    data = 'INIT FLAVOR:Marlin TIME:2019 Filament used: 1.07056m Layer height: 0.2 MINX:90.105 MINY:80.942 MINZ:0.2 MAXX:128.453 MAXY:137.514 MAXZ:26.4 TARGET_MACHINE.NAME:Creality Ender-3 S1 Pr Generated with Cura_SteamEngine 5.6.0  Ender 3 S1 Pro Start G-cod  M413 S0 ; Disable power loss recovery  Prep surfaces before auto home for better accuracy X:-5.00 Y:-5.00 Z:5.00 E:0.00 Count X:-400 Y:-400 Z:2000 LAYER_COUNT:132'
    process.calibrate_data(data)
    print(process.E)
    print(process.layerHeight)
    print(process.minX)
    print(process.minY)
    print(process.minZ)
    print(process.maxX)
    print(process.maxY)
    print(process.maxZ)
    print(process.layerMax)
    