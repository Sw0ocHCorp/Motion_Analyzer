import sys
sys.path.insert(0, "C:\\Users\\nclsr\\OneDrive\\Bureau\\Projets_FabLab_IA\\Motion_Analyzer\\Software")
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Thread_Software.ThreadFilterView import ThreadFilterView
from Windows_UI.PlotWindow import PlotWindow
import numpy as np
from Tasks.MotionAnalyzer import MotionAnalyzer
from Tasks.PlotDataTask import PlotDataTask
from DataAccessController import DataAccessController
from Thread_Software.ThreadVid import ThreadVid
from Thread_Software.DuoPattern.ThreadDuoPattern import ThreadDuoPattern
from Tasks.CsvSaverTask import CsvSaverTask

# --> Classe représentant la fenêtre principale du logiciel
class AnalyzerWindow(QWidget):
    def __init__(self, data_access_controller):             # --* Constructeur: Définition des objets affichés dans la fenêtre et initialisation des tâches
        super().__init__()
        self.data_access_controller= data_access_controller
        self.isDuoCam= self.data_access_controller.get_Duo_Cam()
        self.main_layout= QHBoxLayout()
        self.metric_layout= QVBoxLayout()
        self.vidcap_layout= QVBoxLayout()
        self.plot_window= PlotWindow()

        self.vid_cam= QLabel()
        self.vid_filter= QLabel()
        self.vid_usb= QLabel()
        self.vid_usb_filter= QLabel()
        
        self.setWindowTitle("Analyzer")
        self.setFixedSize(1900, 1000)
        self.metric_layout.addWidget(self.plot_window)
        self.motion_analyzer= MotionAnalyzer(self.data_access_controller, isMain= True)
        self.csv_task= CsvSaverTask(self.data_access_controller)
        self.plot_task= PlotDataTask(self.plot_window, self.data_access_controller)
        self.duo_cam_pattern= ThreadDuoPattern(self.data_access_controller)
        self.thread_duo_streamer= self.duo_cam_pattern.get_usb_streamer()

        self.thread_hardware= ThreadVid(self.data_access_controller)
        self.data_access_controller.adapt_cam_number()
        if self.isDuoCam == False:
            self.thread_hardware.attach_observer(self.motion_analyzer)
            self.thread_hardware.attach_observer(self.plot_task)
            self.thread_hardware.attach_observer(self.csv_task)
            self.thread_hardware.start()
            self.thread_hardware.vid_cam.connect(self.update_vid_cam)
        else:
            self.duo_cam_pattern.attach_observer(self.motion_analyzer)
            self.duo_cam_pattern.attach_observer(self.plot_task)
            self.duo_cam_pattern.attach_observer(self.csv_task)
            self.duo_cam_pattern.start()
            self.thread_duo_streamer.vid_cam.connect(self.update_vid_cam)
            self.thread_duo_streamer.vid_usb.connect(self.update_vid_usb)
        

        self.vidcap_layout.addWidget(self.vid_cam)
        self.vidcap_layout.addWidget(self.vid_usb)
        self.main_layout.addLayout(self.vidcap_layout)
        self.main_layout.addLayout(self.metric_layout)
        self.setLayout(self.main_layout)
        self.show()



    def update_vid_cam(self, img):                          # --* Méthode appelée par le thread de capture vidéo pour mettre à jour l'affichage de la caméra
        self.vid_cam.setPixmap(QPixmap.fromImage(img))
    
    def update_vid_usb(self, img):                          # --* Méthode appelée par le thread de capture vidéo pour mettre à jour l'affichage de la caméra
        self.vid_usb.setPixmap(QPixmap.fromImage(img))


    def closeEvent(self, event):                            # --* Méthode appelée lors de la fermeture de la fenêtre
        if self.isDuoCam == False:
            self.thread_hardware.stop()
        else:
            self.duo_cam_pattern.stop()



if __name__ == '__main__':                                  # TEST INDéPENDANT DE L'INTERFACE                
      
    # creating apyqt5 application
    app = QApplication(sys.argv)
    
    data_controller= DataAccessController()

    # creating a window object
    main = AnalyzerWindow(data_controller)
      
    # showing the window
    main.show()
  
    # loop
    sys.exit(app.exec_())
