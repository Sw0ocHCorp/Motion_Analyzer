import sys
import numpy as np
import time
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2 as cv

class MotionAnalyzer():
    def __init__(self, data_controller):
        self.isInit= False
        self.isActive= True
        self.cam_stream= cv.VideoCapture(0)
        self.blur_coeff= 5
        self.erode_iteration= 5
        self.borne_min= 75
        self.borne_max= 150
        self.refContour= 0
        self.kernel_1= np.array([[0, -1, 0], 
                                 [-1, 8, -1], 
                                 [0, -1, 0]])
        self.big_contour= 0
        self.peri_obj= 0
        #self.loc_memory= np.empty((0, 2), int)
        self.start_timer= time.perf_counter()
        self.data_controller= data_controller
        self.x_motion= self.y_motion= self.deg_angle= 0

    def do_task(self, vid_source):
        self.stream= vid_source
        preprocessed_stream= self.get_preprocess_image()
        return preprocessed_stream

    def save_motion_data(self, i):
        #ACCES AUX DONNEES
        self.data_controller.enable_data_access()
        motion_memory= self.data_controller.get_motion_memory()
        self.data_controller.disable_data_access()
        #ACCES AUX DONNEES
        motion= np.array([motion_memory[i+1, 0] - motion_memory[i, 0], motion_memory[i+1, 1] - motion_memory[i, 1]])
        prev_motion= np.array([motion_memory[i, 0] - motion_memory[i-1, 0], motion_memory[i, 1] - motion_memory[i-1, 1]])
        x_motion= np.abs(motion[0])
        y_motion= np.abs(motion[1])
        if motion_memory[i+1, 0] < motion_memory[i, 0]:
            if motion_memory[i+1, 1] < motion_memory[i, 1]:
                new_x_origin= int(motion_memory[i, 0])
                new_y_origin= int(motion_memory[i, 1])
                new_img_plan= self.stream[new_x_origin:, new_y_origin:]
            else:
                new_x_origin= int(motion_memory[i, 0])
                new_y_origin= int(motion_memory[i, 1])
                new_img_plan= self.stream[0:new_x_origin, new_y_origin:]
        else: 
            prev_motion= -prev_motion
            if motion_memory[i+1, 1] < motion_memory[i, 1]:
                new_x_origin= int(motion_memory[i, 0])
                new_y_origin= int(motion_memory[i, 1])
                new_img_plan= self.stream[new_x_origin:, new_y_origin:]
            else:
                new_x_origin= int(motion_memory[i, 0])
                new_y_origin= int(motion_memory[i, 1])
                new_img_plan= self.stream[0:new_x_origin, new_y_origin:]
        PI= 3.14159
        deg_angle= abs(math.atan2(motion[1], motion[0]) - math.atan2(prev_motion[1], prev_motion[0])) * (180 / PI)
        #ACCES AUX DONNEES
        self.data_controller.enable_data_access()
        self.data_controller.put_motion_data(x_motion, y_motion, deg_angle)
        self.data_controller.disable_data_access()
        #ACCES AUX DONNEES

    def get_preprocess_image(self):
        stream_sh= cv.filter2D(self.stream, -1, self.kernel_1)
        stream_blur= cv.blur(self.stream, (self.blur_coeff, self.blur_coeff))
        stream_erode= cv.erode(stream_blur, None, iterations= self.erode_iteration)
        stream_gray= cv.cvtColor(stream_erode, cv.COLOR_BGR2GRAY)
        stream_sharp= cv.filter2D(stream_gray, -1, self.kernel_1)
        _, thresh_stream= cv.threshold(stream_sharp,0,255, cv.THRESH_OTSU - cv.THRESH_BINARY)
        canny_stream= cv.Canny(thresh_stream, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contours, _= cv.findContours(canny_stream, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            big_contour= max(contours, key= cv.contourArea)                                     #On récupère le plus gros contour 
            x, y, w, h= cv.boundingRect(big_contour)
            bc_size= cv.contourArea(big_contour)
            if cv.contourArea(big_contour) > 50:
                #ACCES AUX DONNEES
                self.data_controller.enable_data_access()
                self.data_controller.put_localisation_data(np.array([[x+(w/2), y+(h/2)]]))
                loc_memory= self.data_controller.get_motion_memory()
                self.data_controller.disable_data_access()
                #ACCES AUX DONNEES
                if (loc_memory.shape[0] > 2):
                    for i in range(loc_memory.shape[0]-1):
                        x1= int(loc_memory[i, 0])
                        y1= int(loc_memory[i, 1])
                        x2= int(loc_memory[i+1, 0])
                        y2= int(loc_memory[i+1, 1])
                        cv.line(self.stream, (x1, y1), (x2, y2), (0, 0, 255-i*10), 3, 8)
                        end_timer= time.perf_counter()
                        if (end_timer - self.start_timer) >= 1:
                            self.start_timer= time.perf_counter()
                            #ACCES AUX DONNEES
                            self.data_controller.enable_data_access()
                            self.save_motion_data(i)
                            self.x_motion, self.y_motion, self.deg_angle= self.data_controller.get_motion_data()
                            self.data_controller.disable_data_access()
                            #ACCES AUX DONNEES
                            #cv.putText(stream, "Distance Objet -> Camera= {:.2f}".format(refContoqqur / CM_XY_1M), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
                cv.rectangle(self.stream, (x, y), (x+w, y+h), (0, 255, 0), 2)                        #On trace le Rectangle correspondant
        cv.putText(self.stream, "Distance Objet -> X axis= {:.2f}, Y axis= {:.2f}, Angle= {:.2f}".format(self.x_motion, self.y_motion, self.deg_angle), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        return self.stream