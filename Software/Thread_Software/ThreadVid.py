from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import cv2 as cv
from Tasks.MotionAnalyzer import MotionAnalyzer
from Tasks.CsvSaverTask import CsvSaverTask

class ThreadVid(QThread):
    vid_cam= pyqtSignal(QImage)
    def __init__(self, data_access_controller):
        super().__init__()
        self.data_access_controller= data_access_controller
        self.observers= np.empty((0,), object)
        self.cam_stream= cv.VideoCapture(0)

    def run(self):
        self.isActive= True
        while self.isActive:
            _, self.stream= self.cam_stream.read()
            for observer in self.observers:
                if isinstance(observer, MotionAnalyzer):
                    self.stream= observer.do_task(self.stream)
                else:
                    if self.data_access_controller.detection == True:
                        observer.do_task()
            self.stream= cv.cvtColor(self.stream, cv.COLOR_BGR2RGB)
            img= QImage(self.stream.data, self.stream.shape[1], self.stream.shape[0], QImage.Format.Format_RGB888)
            img_for_qt= img.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
            self.vid_cam.emit(img)

    def stop(self):
        self.isActive= False
        for observer in self.observers:
                if isinstance(observer, CsvSaverTask):
                    self.stream= observer.end_task()
        print("THREAD VID STOP")
        self.cam_stream.release()
        self.quit()

    def attach_observer(self, observer):
        self.observers= np.append(self.observers, observer)