from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import cv2 as cv
from Tasks.MotionAnalyzer import MotionAnalyzer


class ThreadPatternObserver(QThread):
    img_update= pyqtSignal(QImage)
    def __init__(self, data_access_controler):
        super().__init__()
        self.observers= np.empty((0,), object)
        self.data_controler= data_access_controler
        self.isActive= True
        self.cam_stream= cv.VideoCapture(0)
    def run(self):
        while self.isActive:
            _, stream= self.cam_stream.read()
            if self.data_controler.data_access_is_enable():
                for observer in self.observers:
                    if isinstance(observer, MotionAnalyzer):
                        stream= observer.do_task(stream)
                    else:
                        observer.do_task()
            img= QImage(stream.data, stream.shape[1], stream.shape[0], QImage.Format.Format_RGB888)
            self.img_update.emit(img)
    def stop(self):
        self.isActive= False

    def attach_observer(self, observer):
        self.observers= np.append(self.observers, observer)

    def detach_observer(self, observer):
        self.observers= np.delete(self.observers, observer)

    
