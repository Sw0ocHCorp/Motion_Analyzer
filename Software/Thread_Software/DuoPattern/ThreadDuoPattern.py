from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import cv2 as cv
from Tasks.CsvSaverTask import CsvSaverTask
from DataAccessController import DataAccessController
from Tasks.MotionAnalyzer import MotionAnalyzer
from Thread_Software.DuoPattern.ThreadDuoStreamer import ThreadDuoStreamer

# -->  Thread Pattern Observer || Mode DuoCam
class ThreadDuoPattern(QThread):
    def __init__(self, data_access_controller):
        super().__init__()
        self.data_access_controller= data_access_controller
        self.observers= np.empty((0,), object)
        self.isActive= True
        self.cam_stream= cv.VideoCapture(1)
        self.cam_usb= cv.VideoCapture(0)
        self.thread_duo_streamer= ThreadDuoStreamer()
        self.side_motion_analyzer= MotionAnalyzer(self.data_access_controller, isMain= False)

    def run(self):                                              # --* Méthode permettant de lancer le thread, analyse de mouvement, etc...
        while self.isActive:
            _, self.stream= self.cam_stream.read()
            _, self.stream_usb= self.cam_usb.read()
            
            self.stream_usb= self.side_motion_analyzer.do_task(self.stream_usb)
            self.thread_duo_streamer.set_stream_usb(self.stream_usb)
            for observer in self.observers:
                if isinstance(observer, MotionAnalyzer):
                    self.stream= observer.do_task(self.stream)
                else:
                    if self.data_access_controller.detection == True:
                        observer.do_task()
            self.thread_duo_streamer.set_stream_hardware(self.stream)
            self.thread_duo_streamer.start()
            
            

    def stop(self):                                             # --* Méthode permettant d'arrêter le thread, analyse de mouvement, etc...
        self.isActive= False
        for observer in self.observers:
                if isinstance(observer, CsvSaverTask):
                    self.stream= observer.end_task()
        print("THREAD VID STOP")
        self.cam_stream.release()
        self.cam_usb.release()
        self.isActive= False

    def attach_observer(self, observer):                        # --* Méthode permettable d'ajouter un observer au thread 
        self.observers= np.append(self.observers, observer)
    
    def get_usb_streamer(self):                                 # --* Méthode permettant de récupérer le thread de diffusion des flux vidéo pour l'interface graphique
        return self.thread_duo_streamer
