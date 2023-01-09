from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import cv2 as cv

#--> Thread spécifiquement utilisé pour diffuser les flux vidéo sur l'interface graphique || Mode DuoCam
class ThreadDuoStreamer(QThread):
    vid_cam= pyqtSignal(QImage)
    vid_usb= pyqtSignal(QImage)
    def __init__(self):
        super().__init__()

    def run(self):   
        self.stream_hardware= cv.cvtColor(self.stream_hardware, cv.COLOR_BGR2RGB)
        img= QImage(self.stream_hardware.data, self.stream_hardware.shape[1], self.stream_hardware.shape[0], QImage.Format.Format_RGB888)
        self.vid_cam.emit(img)
        self.stream_usb= cv.cvtColor(self.stream_usb, cv.COLOR_BGR2RGB)
        img_usb= QImage(self.stream_usb.data, self.stream_usb.shape[1], self.stream_usb.shape[0], QImage.Format.Format_RGB888)
        self.vid_usb.emit(img_usb)
    
    def set_stream_usb(self, stream):
        self.stream_usb= stream
    
    def set_stream_hardware(self, stream):
        self.stream_hardware= stream