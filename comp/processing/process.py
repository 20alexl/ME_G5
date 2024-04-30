#comp/processing/process.py

# Code for controlling the image processing
import cv2
import numpy as np
import sys
import os

#from . import process_commands as commands

class ImageProcess:
    def __init__(self):
        self.image = None
        self.printerFlag = str
        self.runnning = bool(True)

        self.master = []
        self.plate = []
        self.build = []
        self.mod = None

        self.layer = None
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
        
        #self.setCommands = commands.Commands()

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
                    self.E = float((init_split[1]))
                if init_split[0] == 'height':
                    init_split[1] = init[l+1].strip()
                    self.layerHeight = float(init_split[1])
                if init_split[0] == 'MINX':
                    self.minX = int(init_split[1])
                if init_split[0] == 'MINY':
                    self.minY = int(init_split[1])
                if init_split[0] == 'MINZ':
                    self.minZ = float(init_split[1])
                if init_split[0] == 'MAXX':
                    self.maxX = int(init_split[1])
                if init_split[0] == 'MAXY':
                    self.maxY = int(init_split[1])
                if init_split[0] == 'MAXZ':
                    self.maxZ = float(init_split[1])
                if init_split[0] == 'LAYER_COUNT':
                    self.layerMax = int(init_split[1])

            #return self.setCommands.get_temperatures()

        except Exception as error:
            raise RuntimeError(f"Error calibrate_data: {error}")
        #READ INIT


    def layer_change(self, layer):
        try:
            self.layer = layer
            return self.setCommands.get_image("therm1")
        except Exception as error:
            raise RuntimeError(f"Error layer_change: {error}")
        #READ LAYER CHANGE


    def canny(self):
        try:
            edges = cv2.Canny(self.mod, 100, 255)
            indices = np.where(edges != [0])
            coordinates = zip(indices[0], indices[1])
            cv2.imshow("Theraml", edges)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return coordinates
        except Exception as error:
            pass


    def findBed(self):
        try:
            self.mod = self.master[self.layer].copy()
            cv2.normalize(self.mod, self.mod, 0, 255, cv2.NORM_MINMAX)
            self.mod = np.uint8(self.mod)
            #self.mod = cv2.applyColorMap(self.mod, cv2.COLORMAP_INFERNO)
            #self.mod = cv2.cvtColor(self.mod, cv2.COLOR_BGR2GRAY)

            #sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            #sharpen = cv2.filter2D(self.mod, -1, sharpen_kernel)

            thresh = cv2.threshold(self.mod, 125, 255, cv2.THRESH_BINARY)[1]
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

            cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            #cv2.imshow('sharpen', sharpen)
            #cv2.imshow('close', close)
            #cv2.imshow('thresh', thresh)
            #cv2.waitKey(0)
            #print(cnts)

            min_area = 8000
            max_area = 11000

            for c in cnts:
                area = int(cv2.contourArea(c))
                #print(area)
                if area > min_area and area < max_area:
                    x,y,w,h = cv2.boundingRect(c)

                    self.mod = self.master[self.layer].copy()
                    self.mod = self.mod[y:y+h, x:x+w]

                    self.plate.append({ #Copy a good plate image to array for storage
                    "image": self.mod.copy(),
                    "x": x,
                    "y": y,
                    "w": w,
                    "h": h
                })

        except Exception as error:
            pass

    def findObject(self):
        try:
            self.mod = self.plate[self.layer].get("image").copy()
            cv2.normalize(self.mod, self.mod, 0, 255, cv2.NORM_MINMAX)
            self.mod = np.uint8(self.mod)
            #self.mod = cv2.blur(self.mod,(5,5),0)
            self.mod = cv2.applyColorMap(self.mod, cv2.COLORMAP_INFERNO)
            self.mod = cv2.cvtColor(self.mod, cv2.COLOR_BGR2GRAY)

            #sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            #sharpen = cv2.filter2D(self.mod, -1, sharpen_kernel)

            thresh = cv2.threshold(self.mod, 145, 255, cv2.THRESH_BINARY)[1]
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

            cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            #cv2.imshow('sharpen', self.mod)
            cv2.imshow('close', close)
            #cv2.imshow('thresh', thresh)
            #cv2.waitKey(0)
            #print(cnts)

            myArea = (self.maxX - self.minX)* (self.maxY - self.minY)
            min_area = (myArea/40) - (myArea/80)
            max_area = (myArea/40) + (myArea/80)
            print(min_area)
            print(max_area)

            for c in cnts:
                area = int(cv2.contourArea(c))
                print(area)
                if area > min_area and area < max_area:
                    x,y,w,h = cv2.boundingRect(c)

                    self.mod = self.master[self.layer].copy()
                    self.mod = self.mod[self.plate[process.layer].get("y") + y:self.plate[process.layer].get("y") + y+h, self.plate[process.layer].get("x") + x:self.plate[process.layer].get("x") + x+w]

                    self.build.append({ #Copy a good plate image to array for storage
                    "image": self.mod.copy(),
                    "x": x,
                    "y": y,
                    "w": w,
                    "h": h
                })
                    return

            self.build.append({ #Copy a good plate image to array for storage
            "image": self.master[self.layer].copy(),
            "x": 0,
            "y": 0,
            "w": 0,
            "h": 0
            })

        except Exception as error:
            pass

    def gradient(self):
        try:
            self.mod = self.plate[self.layer].get("image").copy()
            temp_celsius = ((self.mod / 100)- 273.15)
            bed = int(np.mean(temp_celsius))
            print(bed)
            self.mod = self.build[self.layer].get("image").copy()
            temp_celsius = ((self.mod / 100)- 273.15)
            temp = int(np.mean(temp_celsius))
            print(temp)
            self.temp = bed
            self.bed = temp
        except Exception as error:
            pass

    def LWOI_AMP(self, data, type):
        try:
            if self.layer is None and type != "image":
                cmd_split = data.split("/")
                CalNoz = cmd_split[1].split(' ', 1) #BED TEMP
                self.CalBed = CalBed[0]
                CalBed = cmd_split[2].split(' ', 1) #Nozzel TEMP
                self.CalNozzle = CalNoz[0]
                return None
            elif type == "image":
                image = cv2.medianBlur(data, 5)#used to restore lost image date due to bad frame rate
                sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
                image = cv2.filter2D(image, -1, sharpen_kernel)
                height, width = image.shape[:2]

                top = 1
                bottom = height - 1
                left = 1
                right = width - 1
                image = image[top:bottom, left:right] #Crop image border due to bad framerate(easiest solution)

                self.master.append(image.copy())#Copy a good image to array for storage

                self.findBed()
                self.findObject()
                temp = self.gradient()
                #return self.setCommands.set_bed_temperature(temp)
            else:
                print(data.split())
                return None

        except Exception as error:
            raise RuntimeError(f"Error LWOI_AMP: {error}")
        #LAYER-WISE-OPTICAL-INSPECTION of ADDITIVELY-MANUFACTURED-PARTS
        #READ TEMP DATA
        #COMPARE TO CALIBRATION DATA
        #COMPARE MODEL TEMP TO BED TEMP
        #SET BED TEMP TO MODEL TEMP OR NEAR TO ALLOW MORE EVEN COOLING


    def display_image(self):
        try:
            print(self.layer)
            image = self.master[self.layer].copy()
            if image is not None:
                if image.ndim == 2:
                    cv2.normalize(image, image, 0, 255, cv2.NORM_MINMAX)
                    image = np.uint8(image)
                    image = cv2.applyColorMap(image, cv2.COLORMAP_INFERNO)
                    try:
                        cv2.rectangle(image, (self.plate[self.layer].get("x"), self.plate[self.layer].get("y")), (self.plate[self.layer].get("x") + self.plate[self.layer].get("w"), self.plate[self.layer].get("y") + self.plate[self.layer].get("h")), (36,255,12), 2)
                        cv2.rectangle(image, (self.plate[self.layer].get("x") + self.build[self.layer].get("x"), self.plate[self.layer].get("y") + self.build[self.layer].get("y")), (self.build[self.layer].get("x") + self.plate[self.layer].get("x") + self.build[self.layer].get("w"), self.build[self.layer].get("y") + self.plate[self.layer].get("y") + self.build[self.layer].get("h")), (36,255,12), 2)
                    except Exception as error:
                        pass
                    cv2.imshow("Thermal", image)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                else:
                    cv2.imshow("RGB", image)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
            else:
                raise RuntimeError("No image to display")
        except Exception as error:
            raise RuntimeError(f"Error displaying image: {error}")
        

if __name__ == "__main__":
    process = ImageProcess()
    process.layer = 0
    process.minX = 92
    process.minY = 91
    process.maxX = 128
    process.maxY = 138

    current_dir = os.getcwd()
    relative_folder_path = "test_images"
    image_filename = "60deg_bed1.png"
    image_filename = "cold_object1.png"
    image_filename = "residual2.png"
    image_filename = "Layer10.png"
    image_path = os.path.join(current_dir, relative_folder_path, image_filename)
    image = cv2.imread(image_path, cv2.IMREAD_ANYDEPTH)
    print(image.dtype)

    if image is not None:
        print("Image was successfully read.")
        # Display the image
        cv2.imshow("Image", image)
        cv2.waitKey(1)
        cv2.destroyAllWindows()
    else:
        print("Failed to read the image.")

    process.LWOI_AMP(image, "image")
    process.display_image()
    # mod = process.master[process.layer].copy()
    # cv2.rectangle(mod, (process.plate[process.layer].get("x"), process.plate[process.layer].get("y")), (process.plate[process.layer].get("x") + process.plate[process.layer].get("w"), process.plate[process.layer].get("y") + process.plate[process.layer].get("h")), (36,255,12), 2)
    # cv2.rectangle(mod, (process.plate[process.layer].get("x") + process.build[process.layer].get("x"), process.plate[process.layer].get("y") + process.build[process.layer].get("y")), (process.build[process.layer].get("x") + process.plate[process.layer].get("x") + process.build[process.layer].get("w"), process.build[process.layer].get("y") + process.plate[process.layer].get("y") + process.build[process.layer].get("h")), (36,255,12), 2)
    # cv2.imshow("RGB", mod)
    # cv2.waitKey(0)

    # mod = process.plate[process.layer].get("image").copy()
    # cv2.imshow("RGB", mod)
    # cv2.waitKey(0)

    # mod = process.build[process.layer].get("image").copy()
    # cv2.imshow("RGB", mod)
    # cv2.waitKey(0)


    # data = 'INIT FLAVOR:Marlin TIME:2019 Filament used: 1.07056m Layer height: 0.2 MINX:90.105 MINY:80.942 MINZ:0.2 MAXX:128.453 MAXY:137.514 MAXZ:26.4 TARGET_MACHINE.NAME:Creality Ender-3 S1 Pr Generated with Cura_SteamEngine 5.6.0  Ender 3 S1 Pro Start G-cod  M413 S0 ; Disable power loss recovery  Prep surfaces before auto home for better accuracy X:-5.00 Y:-5.00 Z:5.00 E:0.00 Count X:-400 Y:-400 Z:2000 LAYER_COUNT:132'
    # process.calibrate_data(data)
    # print(process.E)
    # print(process.layerHeight)
    # print(process.minX)
    # print(process.minY)
    # print(process.minZ)
    # print(process.maxX)
    # print(process.maxY)
    # print(process.maxZ)
    # print(process.layerMax)
    