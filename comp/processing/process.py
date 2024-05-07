#comp/processing/process.py

# Code for controlling the image processing
import cv2
import numpy as np
import sys
import os
import datetime

from . import process_commands as commands

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
        self.superBed = 0
        
        self.setCommands = commands.Commands()

    def calibrate_data(self, init):
        try:
            #init = init.strip('INIT ')
            init = init.split()
            for l in range(len(init)):
                init_split = init[l].split(':')
                init_split[0] = init_split[0].strip()
                #print(init_split)
                if init_split[0] == 'used':
                    init[l+1] = init[l+1].strip()
                    init_split[1] = init[l+1].strip('m')
                    self.E = float((init_split[1]))
                if init_split[0] == 'height':
                    init_split[1] = init[l+1].strip()
                    self.layerHeight = float(init_split[1])
                if init_split[0] == 'MINX':
                    self.minX = int(float(init_split[1]))
                if init_split[0] == 'MINY':
                    self.minY = int(float(init_split[1]))
                if init_split[0] == 'MINZ':
                    self.minZ = float(init_split[1])
                if init_split[0] == 'MAXX':
                    self.maxX = int(float(init_split[1]))
                if init_split[0] == 'MAXY':
                    self.maxY = int(float(init_split[1]))
                if init_split[0] == 'MAXZ':
                    self.maxZ = float(init_split[1])
                if init_split[0] == 'LAYER_COUNT':
                    self.layerMax = int(float(init_split[1]))

            print("FILAMENT USED: " + str(self.E))
            # print(self.layerHeight)
            # print(self.minX)
            # print(self.minY)
            # print(self.minZ)
            # print(self.maxX)
            # print(self.maxY)
            # print(self.maxZ)
            # print(self.layerMax)

        except Exception as error:
            raise RuntimeError(f"Error calibrate_data: {error}")
        #READ INIT

    def layer_change(self, layer):
        try:
            if layer == '0':
                self.layer = 0
            else:
                self.layer = int(layer)
            print("============LAYER: " + str(self.layer) + "============")
            return self.setCommands.get_image("therm1")
        except Exception as error:
            raise RuntimeError(f"Error layer_change: {error}")
        #READ LAYER CHANGE

    def findBed(self):
        try:
            self.mod = self.master[self.layer].copy()
            cv2.normalize(self.mod, self.mod, 0, 255, cv2.NORM_MINMAX)
            self.mod = np.uint8(self.mod)
            self.image = self.mod.copy()

            # print("1")
            thresh = cv2.threshold(self.mod, 150, 255, cv2.THRESH_BINARY)[1]
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

            cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            min_area = 8000
            max_area = 11000

            for c in cnts:
                area = int(cv2.contourArea(c))
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
                    return

            # print("2")
            self.mod = self.image.copy()
            thresh = cv2.threshold(self.mod, 150, 255, cv2.THRESH_BINARY)[1]
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

            cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            min_area = 8000
            max_area = 11000

            for c in cnts:
                area = int(cv2.contourArea(c))
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
                    return
            
            # print("final bed")
            self.mod = self.master[self.layer].copy()
            self.plate.append({ #Copy a good plate image to array for storage if not object found
            "image": self.mod.copy(),
            "x": 0,
            "y": 0,
            "w": 0,
            "h": 0
            })

        except Exception as error:
            print(error)
            pass

    def findObject(self):
        try:
            self.mod = self.plate[self.layer].get("image").copy()
            height, width = self.mod.shape[:2]

            crop = 20
            top = crop
            bottom = height - crop
            left = crop
            right = width - crop
            self.mod = self.mod[top:bottom, left:right] #Crop image border due to bad framerate(easiest solution)

            cv2.normalize(self.mod, self.mod, 0, 255, cv2.NORM_MINMAX)
            self.mod = np.uint8(self.mod)
            self.image = self.mod.copy()

            #Try First attempt
            thresh = cv2.threshold(self.mod, 140, 255, cv2.THRESH_BINARY)[1]
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

            cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            #cv2.imshow('sharpen', self.mod)
            #cv2.imshow('close', close)
            #cv2.imshow('thresh', thresh)
            #cv2.waitKey(0)
            #print(cnts)

            myArea = (self.maxX - self.minX) * (self.maxY - self.minY)
            min_area = int((myArea/40) - (myArea/50))
            max_area = int((myArea/40) + (myArea/50))
            # print(min_area)
            # print(max_area)
            # print("1")

            for c in cnts:
                area = int(cv2.contourArea(c))
                if area > min_area and area < max_area:
                    x,y,w,h = cv2.boundingRect(c)

                    self.mod = self.master[self.layer].copy()
                    self.mod = self.mod[self.plate[self.layer].get("y") + y + crop:self.plate[self.layer].get("y") + y + h + crop, self.plate[self.layer].get("x") + x + crop:self.plate[self.layer].get("x") + x + w + crop]

                    self.build.append({ #Copy a good plate image to array for storage
                    "image": self.mod.copy(),
                    "x": x + crop,
                    "y": y + crop,
                    "w": w,
                    "h": h
                })
                    return
                
            #Try Second attempt
            self.mod = self.image.copy()
            thresh = cv2.threshold(self.mod, 100, 255, cv2.THRESH_BINARY_INV)[1]
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

            cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            #cv2.imshow('sharpen', self.mod)
            #cv2.imshow('close', close)
            #cv2.imshow('thresh', thresh)
            #cv2.waitKey(0)
            #print(cnts)

            myArea = (self.maxX - self.minX) * (self.maxY - self.minY)
            min_area = int((myArea/40) - (myArea/55))
            max_area = int((myArea/40) + (myArea/55))
            # print(min_area)
            # print(max_area)
            # print("2")

            for c in cnts:
                area = int(cv2.contourArea(c))
                if area > min_area and area < max_area:
                    x,y,w,h = cv2.boundingRect(c)

                    self.mod = self.master[self.layer].copy()
                    self.mod = self.mod[self.plate[self.layer].get("y") + y + crop:self.plate[self.layer].get("y") + y + h + crop, self.plate[self.layer].get("x") + x + crop:self.plate[self.layer].get("x") + x + w + crop]

                    self.build.append({ #Copy a good plate image to array for storage
                    "image": self.mod.copy(),
                    "x": x + crop,
                    "y": y + crop,
                    "w": w,
                    "h": h
                })
                    return

            #Try Third attempt
            self.mod = self.image.copy()
            height, width = self.mod.shape[:2]

            aveX = int((self.minX + self.maxX)/2)
            aveY = int((self.minY + self.maxY)/2)
            distX = int((self.maxX - self.minX)/2)
            distY = int((self.maxY - self.minY)/2)
            buff = 10

            top = int(aveX/2 - distX - buff)
            bottom = height - top
            left = int(aveY/2 - distY - buff)
            right = width - left

            #print(str(top) + "top" + str(bottom) + "top" + str(left) + "top" + str(right)+ "top" + str(aveX)+ "top" + str(aveY)+ "top" + str(distX)+ "top" + str(distY))

            self.mod = self.mod[top:bottom, left:right] #Crop image border due to bad framerate(easiest solution)
            thresh = cv2.threshold(self.mod, 100, 255, cv2.THRESH_BINARY_INV)[1]
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            close = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel, iterations=1)

            cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            #cv2.imshow('sharpen', self.mod)
            #cv2.imshow('close', close)
            #cv2.imshow('thresh', thresh)
            #cv2.waitKey(0)
            #print(cnts)

            myArea = (self.maxX - self.minX) * (self.maxY - self.minY)
            min_area = int((myArea/40) - (myArea/60))
            max_area = int((myArea/40) + (myArea/75))
            # print(min_area)
            # print(max_area)
            # print("3")

            for c in cnts:
                area = int(cv2.contourArea(c))
                if area > min_area and area < max_area:
                    x,y,w,h = cv2.boundingRect(c)

                    self.mod = self.master[self.layer].copy()
                    self.mod = self.mod[self.plate[self.layer].get("y") + y + top:self.plate[self.layer].get("y") + y + h + bottom, self.plate[self.layer].get("x") + x + left:self.plate[self.layer].get("x") + x + w + right]

                    self.build.append({ #Copy a good plate image to array for storage
                    "image": self.mod.copy(),
                    "x": x + crop + left,
                    "y": y + crop + top,
                    "w": w,
                    "h": h
                })
                    return

            self.mod = self.plate[self.layer].get("image").copy()
            self.build.append({ #Copy a good plate image to array for storage if not object found
            "image": self.mod.copy(),
            "x": 0,
            "y": 0,
            "w": 0,
            "h": 0
            })

        except Exception as error:
            print(error)
            pass

    def gradient(self):
        try:
            self.mod = self.plate[self.layer].get("image").copy()
            temp_celsius = ((self.mod / 100)- 273.15)
            bed = int(np.median(temp_celsius))
            print("BED " + str(bed))
            self.mod = self.build[self.layer].get("image").copy()
            temp_celsius = ((self.mod / 100)- 273.15)
            temp = int(np.mean(temp_celsius))
            print("TEMP: " + str(temp))
            self.temp = bed
            self.bed = temp
            kP = 4

            if self.layer > int(self.layerMax/2):
                self.superBed = self.superBed - 2
                if self.superBed < 35:
                    self.superBed = 45

            if self.bed > self.CalBed and self.temp > self.CalBed: #BED HOT PRINT HOT
                self.CalBed = self.CalBed - abs(int((self.bed - self.temp)/kP))
                if self.CalBed > self.superBed:
                    self.CalBed = self.superBed
                return self.CalBed #COOL
            elif self.bed > self.CalBed and self.temp < self.CalBed: #BED HOT PRINT COLD
                self.CalBed = self.CalBed - int((self.bed - self.temp)/kP)
                if self.CalBed > self.superBed:
                    self.CalBed = self.superBed
                return self.CalBed #COOL
            elif self.bed < self.CalBed and self.temp < self.CalBed: #BED COLD PRINT COLD
                self.CalBed = self.CalBed + abs(int((self.bed - self.temp)/kP))
                if self.CalBed > self.superBed:
                    self.CalBed = self.superBed
                return self.CalBed #HEAT
            elif self.bed < self.CalBed and self.temp > self.CalBed: #BED COLD PRINT HOT
                self.CalBed = self.CalBed + int((self.temp - self.bed)/kP)
                if self.CalBed > self.superBed:
                    self.CalBed = self.superBed
                return self.CalBed #HEAT
            else:
                return self.CalBed

        except Exception as error:
            pass

    def LWOI_AMP(self, data, type):
        try:
            if self.layer == 0 and type != "image":
                cmd_split = data.split('/')
                CalNoz = cmd_split[1].split(' ', 1) #BED TEMP
                CalBed = cmd_split[2].split(' ', 1) #Nozzel TEMP
                self.CalNozzle = int(float(CalNoz[0]))
                self.CalBed = int(float(CalBed[0])) + int(((int(float(CalBed[0])) - self.bed))/2)
                self.superBed = self.CalBed + 10
                print(str(self.CalBed))
                print(str(self.CalNozzle))
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
                self.save_current()
                #self.display_image()
                temp = self.gradient()

                if self.layer == 0:
                    return self.setCommands.get_temperatures()

                if temp is None:
                    return None
                else:
                    #print(temp)
                    return self.setCommands.set_bed_temperature(temp)
            else:
                #print(data.split())
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
            #print(self.layer)
            master = self.master[self.layer].copy()
            if master is not None:
                if master.ndim == 2:
                    cv2.normalize(master, master, 0, 255, cv2.NORM_MINMAX)
                    master = np.uint8(master)
                    master = cv2.applyColorMap(master, cv2.COLORMAP_INFERNO)
                    try:
                        cv2.rectangle(master, (self.plate[self.layer].get("x"), self.plate[self.layer].get("y")), (self.plate[self.layer].get("x") + self.plate[self.layer].get("w"), self.plate[self.layer].get("y") + self.plate[self.layer].get("h")), (36,255,12), 2)
                        cv2.rectangle(master, (self.plate[self.layer].get("x") + self.build[self.layer].get("x"), self.plate[self.layer].get("y") + self.build[self.layer].get("y")), (self.build[self.layer].get("x") + self.plate[self.layer].get("x") + self.build[self.layer].get("w"), self.build[self.layer].get("y") + self.plate[self.layer].get("y") + self.build[self.layer].get("h")), (36,255,12), 2)
                    except Exception as error:
                        pass
                    master = cv2.resize(master, None, fx=5, fy=5)
                    cv2.imshow('MASTER', master)

                    try:
                        plate = self.plate[self.layer].get("image").copy()
                        cv2.normalize(plate, plate, 0, 255, cv2.NORM_MINMAX)
                        plate = np.uint8(plate)
                        plate = cv2.applyColorMap(plate, cv2.COLORMAP_INFERNO)
                        plate = cv2.resize(plate, None, fx=5, fy=5)
                        cv2.imshow('PLATE', plate)
                    except Exception as error:
                        pass

                    try:
                        build = self.build[self.layer].get("image").copy()
                        cv2.normalize(build, build, 0, 255, cv2.NORM_MINMAX)
                        build = np.uint8(build)
                        build = cv2.applyColorMap(build, cv2.COLORMAP_INFERNO)
                        build = cv2.resize(build, None, fx=10, fy=10)
                        cv2.imshow('BUILD', build)
                    except Exception as error:
                        pass
                    
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                else:
                    cv2.imshow("RGB", master)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
            else:
                raise RuntimeError("No image to display")
        except Exception as error:
            raise RuntimeError(f"Error displaying image: {error}")

    def save_current(self):
        try:

            current_dir = os.getcwd()
            folder_path = os.path.join(current_dir, "runs", "current")
            os.makedirs(folder_path, exist_ok=True)

            print("Length of self.master:", len(self.master))
            print("Length of self.plate:", len(self.plate))
            print("Length of self.build:", len(self.build))
            print("Current layer:", self.layer)
            #GRAY

            folder_path = os.path.join(current_dir, "runs", "current", "GRAY")
            os.makedirs(folder_path, exist_ok=True)

            folder_path = os.path.join(current_dir, "runs", "current", "GRAY", "master")
            os.makedirs(folder_path, exist_ok=True)

            image = self.master[self.layer].copy()
            filename = os.path.join(folder_path, f"LAYER_{self.layer}.png")
            image = cv2.resize(image, None, fx=10, fy=10)
            cv2.imwrite(filename, image)

            folder_path = os.path.join(current_dir, "runs", "current", "GRAY", "plate")
            os.makedirs(folder_path, exist_ok=True)

            image = self.plate[self.layer].get("image").copy()
            filename = os.path.join(folder_path, f"LAYER_{self.layer}.png")
            image = cv2.resize(image, None, fx=10, fy=10)
            cv2.imwrite(filename, image)

            folder_path = os.path.join(current_dir, "runs", "current", "GRAY", "build")
            os.makedirs(folder_path, exist_ok=True)

            image = self.build[self.layer].get("image").copy()
            filename = os.path.join(folder_path, f"LAYER_{self.layer}.png")
            image = cv2.resize(image, None, fx=10, fy=10)
            cv2.imwrite(filename, image)

            #RGB

            folder_path = os.path.join(current_dir, "runs", "current", "RGB")
            os.makedirs(folder_path, exist_ok=True)

            folder_path = os.path.join(current_dir, "runs", "current", "RGB", "master")
            os.makedirs(folder_path, exist_ok=True)

            image = self.master[self.layer].copy()
            cv2.normalize(image, image, 0, 255, cv2.NORM_MINMAX)
            image = np.uint8(image)
            image = cv2.applyColorMap(image, cv2.COLORMAP_INFERNO)
            try:
                cv2.rectangle(image, (self.plate[self.layer].get("x"), self.plate[self.layer].get("y")), (self.plate[self.layer].get("x") + self.plate[self.layer].get("w"), self.plate[self.layer].get("y") + self.plate[self.layer].get("h")), (36,255,12), 2)
                cv2.rectangle(image, (self.plate[self.layer].get("x") + self.build[self.layer].get("x"), self.plate[self.layer].get("y") + self.build[self.layer].get("y")), (self.build[self.layer].get("x") + self.plate[self.layer].get("x") + self.build[self.layer].get("w"), self.build[self.layer].get("y") + self.plate[self.layer].get("y") + self.build[self.layer].get("h")), (36,255,12), 2)
            except Exception as error:
                pass
            image = cv2.resize(image, None, fx=10, fy=10)
            filename = os.path.join(folder_path, f"LAYER_{self.layer}.png")
            cv2.imwrite(filename, image)

            folder_path = os.path.join(current_dir, "runs", "current", "RGB", "plate")
            os.makedirs(folder_path, exist_ok=True)

            image = self.plate[self.layer].get("image").copy()
            cv2.normalize(image, image, 0, 255, cv2.NORM_MINMAX)
            image = np.uint8(image)
            image = cv2.applyColorMap(image, cv2.COLORMAP_INFERNO)
            image = cv2.resize(image, None, fx=10, fy=10)
            filename = os.path.join(folder_path, f"LAYER_{self.layer}.png")
            cv2.imwrite(filename, image)

            folder_path = os.path.join(current_dir, "runs", "current", "RGB", "build")
            os.makedirs(folder_path, exist_ok=True)

            image = self.build[self.layer].get("image").copy()
            cv2.normalize(image, image, 0, 255, cv2.NORM_MINMAX)
            image = np.uint8(image)
            image = cv2.applyColorMap(image, cv2.COLORMAP_INFERNO)
            image = cv2.resize(image, None, fx=15, fy=15)
            filename = os.path.join(folder_path, f"LAYER_{self.layer}.png")
            cv2.imwrite(filename, image)

        except Exception as error:
            raise RuntimeError(f"Error saving current image: {error}")


    def save_run(self):
        try:
            ct = datetime.datetime.now()
            ct = str(ct.timestamp())
            current_dir = os.getcwd()
            folder_path = os.path.join(current_dir, "runs", ct)
            os.makedirs(folder_path, exist_ok=True)

            #GRAY

            folder_path = os.path.join(current_dir, "runs", ct, "GRAY")
            os.makedirs(folder_path, exist_ok=True)

            folder_path = os.path.join(current_dir, "runs", ct, "GRAY", "master")
            os.makedirs(folder_path, exist_ok=True)

            for i, image in enumerate(self.master):
                filename = os.path.join(folder_path, f"LAYER_{i}.png")
                image = cv2.resize(image, None, fx=10, fy=10)
                cv2.imwrite(filename, image)

            # folder_path = os.path.join(current_dir, "runs", ct, "GRAY", "plate")
            # os.makedirs(folder_path, exist_ok=True)

            # for i, image_dict in enumerate(self.plate):
            #     image = image_dict["image"]
            #     image = cv2.resize(image, None, fx=10, fy=10)
            #     filename = os.path.join(folder_path, f"LAYER_{i}.png")
            #     cv2.imwrite(filename, image)

            # folder_path = os.path.join(current_dir, "runs", ct, "GRAY", "build")
            # os.makedirs(folder_path, exist_ok=True)

            # for i, image_dict in enumerate(self.build):
            #     image = image_dict["image"]
            #     image = cv2.resize(image, None, fx=10, fy=10)
            #     filename = os.path.join(folder_path, f"LAYER_{i}.png")
            #     cv2.imwrite(filename, image)

            #RGB

            folder_path = os.path.join(current_dir, "runs", ct, "RGB")
            os.makedirs(folder_path, exist_ok=True)

            folder_path = os.path.join(current_dir, "runs", ct, "RGB", "master")
            os.makedirs(folder_path, exist_ok=True)

            for i, image in enumerate(self.master):
                filename = os.path.join(folder_path, f"LAYER_{i}.png")
                cv2.normalize(image, image, 0, 255, cv2.NORM_MINMAX)
                image = np.uint8(image)
                image = cv2.applyColorMap(image, cv2.COLORMAP_INFERNO)
                image = cv2.resize(image, None, fx=10, fy=10)
                cv2.imwrite(filename, image)

            folder_path = os.path.join(current_dir, "runs", ct, "RGB", "plate")
            os.makedirs(folder_path, exist_ok=True)

            for i, image_dict in enumerate(self.plate):
                image = image_dict["image"]
                cv2.normalize(image, image, 0, 255, cv2.NORM_MINMAX)
                image = np.uint8(image)
                image = cv2.applyColorMap(image, cv2.COLORMAP_INFERNO)
                image = cv2.resize(image, None, fx=10, fy=10)
                filename = os.path.join(folder_path, f"LAYER_{i}.png")
                cv2.imwrite(filename, image)

            folder_path = os.path.join(current_dir, "runs", ct, "RGB", "build")
            os.makedirs(folder_path, exist_ok=True)

            for i, image_dict in enumerate(self.build):
                image = image_dict["image"]
                cv2.normalize(image, image, 0, 255, cv2.NORM_MINMAX)
                image = np.uint8(image)
                image = cv2.applyColorMap(image, cv2.COLORMAP_INFERNO)
                image = cv2.resize(image, None, fx=10, fy=10)
                filename = os.path.join(folder_path, f"LAYER_{i}.png")
                cv2.imwrite(filename, image)

        except Exception as error:
            raise RuntimeError(f"Error saving run: {error}")


if __name__ == "__main__":
    process = ImageProcess()
    process.CalBed = 50
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
    image_filename = "Layer100.png"
    image_path = os.path.join(current_dir, relative_folder_path, image_filename)
    image = cv2.imread(image_path, cv2.IMREAD_ANYDEPTH)

    if image is not None:
        print("Image was successfully read.")
        # Display the image
    else:
        print("Failed to read the image.")

    process.LWOI_AMP(image, "image")
    #process.save_current()
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
    