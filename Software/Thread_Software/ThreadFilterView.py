from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import cv2 as cv

class ThreadFilterView(QThread):
    vid_cam= pyqtSignal(QImage)
    vid_filter= pyqtSignal(QImage)
    def __init__(self, data_access_controller, vidChannel):
        super().__init__()
        self.data_access_controller= data_access_controller
        self.isInit= False
        self.isActive= True
        self.cam_stream= cv.VideoCapture(vidChannel)
        self.blur_coeff= 5
        self.erode_iteration= 5
        self.borne_min= 75
        self.borne_max= 150
        self.refContour= 0
        self.big_contour= 0
        self.val_max= 255
        self.threshold= 0

    def run(self):   
        while self.isActive:
            try:
                _, self.stream= self.cam_stream.read()
                stream= cv.cvtColor(self.stream, cv.COLOR_BGR2RGB)
                canny_stream= self.get_threshold_stream(self.stream)
                img= QImage(stream.data, stream.shape[1], stream.shape[0], QImage.Format.Format_RGB888)
                self.vid_cam.emit(img)
                img= QImage(canny_stream.data, canny_stream.shape[1], canny_stream.shape[0], QImage.Format.Format_Grayscale8)
                self.vid_filter.emit(img)
            except:
                pass

    def stop(self):
        self.cam_stream.release()
        self.isActive= False

    def get_threshold_stream(self, source_stream):
        stream_blur= cv.blur(source_stream, (self.blur_coeff, self.blur_coeff))
        stream_erode= cv.erode(stream_blur, None, iterations= self.erode_iteration)
        stream_gray= cv.cvtColor(stream_erode, cv.COLOR_BGR2GRAY)
        self.cent_val= self.data_access_controller.get_kernel()[1,1]
        stream_sharp= cv.filter2D(stream_gray, -1, self.data_access_controller.get_kernel())
        thresh_mode= self.data_access_controller.get_thresh_method()
        _, thresh_stream= cv.threshold(stream_sharp, self.threshold,
                                                self.val_max, cv.THRESH_OTSU - cv.THRESH_BINARY)
        if thresh_mode == 1:
            thresh_stream= cv.adaptiveThreshold(stream_sharp,255,cv.ADAPTIVE_THRESH_MEAN_C,\
                                                        cv.THRESH_BINARY,11,2)
        elif thresh_mode == 2:
            thresh_stream= cv.adaptiveThreshold(stream_sharp,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                                    cv.THRESH_BINARY,11,2)
        canny_stream= cv.Canny(thresh_stream, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        return canny_stream

