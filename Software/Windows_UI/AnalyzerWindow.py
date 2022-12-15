import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
sys.path.insert(0, "C:\\Users\\nclsr\\OneDrive\\Bureau\\Projets_FabLab_IA\\Motion_Analyzer\\Software")
import matplotlib
from Windows_UI.PlotWindow import PlotWindow
matplotlib.use('Qt5Agg')
import numpy as np
from Thread_Software.ThreadPatternObserver import ThreadPatternObserver
from Tasks.MotionAnalyzer import MotionAnalyzer
from Tasks.PlotDataTask import PlotDataTask
from DataAccessController import DataAccessController
from Thread_Software.ThreadVid import ThreadVid
from Tasks.CsvSaverTask import CsvSaverTask

class AnalyzerWindow(QMainWindow):
    def __init__(self, data_access_controller):
        super().__init__()
        self.setWindowTitle("Motion Analyzer")
        self.setGeometry(0, 0, 1900, 1000)
        self.main_layout= QHBoxLayout()
        self.metric_layout= QVBoxLayout()
        self.vidcap_layout= QVBoxLayout()
        self.video_label= QLabel()
        self.plot_window= PlotWindow()
        self.main_widget= QWidget()
        self.vidcap_layout.addWidget(self.video_label)
        self.metric_layout.addWidget(self.plot_window)
        self.data_controller= data_access_controller
        self.motion_analyzer= MotionAnalyzer(self.data_controller)
        self.csv_task= CsvSaverTask(self.data_controller)
        self.plot_task= PlotDataTask(self.plot_window, self.data_controller)
        self.thread_vid= ThreadVid(self.data_controller)
        self.thread_vid.attach_observer(self.motion_analyzer)
        self.thread_vid.attach_observer(self.plot_task)
        self.thread_vid.attach_observer(self.csv_task)
        self.thread_vid.start()
        self.thread_vid.image_update.connect(self.updateVideo)
        self.main_layout.addLayout(self.vidcap_layout)
        self.main_layout.addLayout(self.metric_layout)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
    
    def updateVideo(self, img):
        self.video_label.setPixmap(QPixmap.fromImage(img))
    
    def closeEvent(self, event):
        self.thread_vid.stop()