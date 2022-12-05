import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib
from PlotWindow import PlotWindow
matplotlib.use('Qt5Agg')
import numpy as np
from Thread_Software.ThreadPatternObserver import ThreadPatternObserver
from Tasks.MotionAnalyzer import MotionAnalyzer
from Thread_Software.DataAccessController import DataAccessController

class AnalyzerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Motion Analyzer")
        self.setGeometry(0, 0, 1900, 1000)
        self.main_layout= QHBoxLayout()
        self.metric_layout= QVBoxLayout()
        self.vidcap_layout= QVBoxLayout()
        self.video_label= QLabel()
        self.plot_window= PlotWindow()
        self.plot_window.plot_data(np.array([0, 1]), np.array([0, 1]))
        self.vidcap_layout.addWidget(self.video_label)
        self.metric_layout.addWidget(self.plot_window)
        self.data_controller= DataAccessController()
        self.motion_analyzer= MotionAnalyzer(self.data_controller)
        self.pattern_observer= ThreadPatternObserver(self.data_controller)
        self.pattern_observer.attach_observer(self.motion_analyzer)
        self.pattern_observer.img_update.connect(self.updateVideo)
        self.pattern_observer.start()
        self.main_layout.addLayout(self.vidcap_layout)
        #self.main_layout.addLayout(self.metric_layout)
        self.setLayout(self.main_layout)
    
    def updateVideo(self, img):
        self.video_label.setPixmap(QPixmap.fromImage(img))
    
    def closeEvent(self):
        self.pattern_observer.stop()