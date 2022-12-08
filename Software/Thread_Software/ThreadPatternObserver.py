from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import cv2 as cv
from Tasks.MotionAnalyzer import MotionAnalyzer


class ThreadPatternObserver(QThread):
    img_update= pyqtSignal(QImage)
    observers= np.empty((0,), object)
    def __init__(self, data_access_controller):
        super().__init__()
        self.data_controller= data_access_controller
    def run(self):
        print("THREAD PATTERN OBSERVER RUN= ", self.data_controller.stream_access_is_enable())
        if self.data_controller.stream_access_is_enable():
            self.data_controller.enable_stream_access()
            stream= self.data_controller.get_stream()
            for observer in self.observers:
                if isinstance(observer, MotionAnalyzer):
                    stream= observer.do_task(stream)
                else:
                    observer.do_task()
            self.data_controller.disable_stream_access()

    def attach_observer(self, observer):
        self.observers= np.append(self.observers, observer)

    def detach_observer(self, observer):
        self.observers= np.delete(self.observers, observer)

    
