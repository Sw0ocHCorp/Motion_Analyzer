import sys
sys.path.insert(0, "C:\\Users\\nclsr\\OneDrive\\Bureau\\Projets_FabLab_IA\\Motion_Analyzer\\Software")
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Thread_Software.ThreadFilterView import ThreadFilterView
from DataAccessController import DataAccessController
from Windows_UI.AnalyzerWindow import AnalyzerWindow
import numpy as np

class ParamsWindow(QWidget):
    def __init__(self, data_access_controller):
        super().__init__()
        self.data_access_controller= data_access_controller
        self.cent_val= 8
        self.kernel= np.array(  [[0, -1, 0], 
                                     [-1, self.cent_val, -1], 
                                     [0, -1, 0]])
        self.prev_id= 1

        self.main_layout= QHBoxLayout()
        self.button_layout= QHBoxLayout()
        self.rad_button_layout= QHBoxLayout()
        self.vidcap_layout= QVBoxLayout()
        self.metric_layout= QVBoxLayout()
        self.mode_layout= QVBoxLayout()
        self.thresh_layout= QVBoxLayout()
        self.thresh_layout.setContentsMargins(0, 15, 0, 15)
        self.vid_filter= QLabel()
        self.measure_unit= QTextEdit()
        self.valid_button= QPushButton("Valider")
        self.more_button= QPushButton("Accentuer")
        self.less_button= QPushButton("Réduire")
        self.rad_smooth= QRadioButton("Lisser l'image")
        self.rad_sharp= QRadioButton("Accentuer les contours")
        self.button_group = QButtonGroup()
        self.rad_sharp.setChecked(True)
        self.button_group.addButton(self.rad_smooth, 0)
        self.button_group.addButton(self.rad_sharp, 1)
        self.method_group = QButtonGroup()
        self.thresh_basic= QRadioButton("Classique")
        self.thresh_mean= QRadioButton("Moyenne")
        self.thresh_gaussian= QRadioButton("Gaussien")
        self.thresh_basic.setChecked(True)
        self.method_group.addButton(self.thresh_basic, 0)
        self.method_group.addButton(self.thresh_mean, 1)
        self.method_group.addButton(self.thresh_gaussian, 2)
        self.method_group.buttonClicked.connect(self.update_method)
        self.more_button.clicked.connect(self.up_kernel)
        self.less_button.clicked.connect(self.low_kernel)
        self.valid_button.clicked.connect(self.update_all_params)
        self.setWindowTitle("Params")
        self.setFixedSize(1200, 800)
        self.thread_param_filter= ThreadFilterView(data_access_controller)
        self.metric_layout.addWidget(QLabel("Choisissez l'unité de références \npour le Calcul de Vitesse / Accélération (en ms)"))
        self.metric_layout.addWidget(self.measure_unit)
        self.thresh_layout.addWidget(QLabel("Choisir la méthode de seuillage:"))
        self.thresh_layout.addWidget(self.thresh_basic)
        self.thresh_layout.addWidget(self.thresh_mean)
        self.thresh_layout.addWidget(self.thresh_gaussian)
        self.metric_layout.addLayout(self.thresh_layout)
        self.rad_button_layout.addWidget(self.rad_smooth)
        self.rad_button_layout.addWidget(self.rad_sharp)
        self.mode_layout.addLayout(self.rad_button_layout)
        self.button_layout.addWidget(self.more_button)
        self.button_layout.addWidget(self.less_button)
        self.button_layout.addWidget(self.valid_button)
        self.mode_layout.addLayout(self.button_layout)
        self.vidcap_layout.addWidget(self.vid_filter)
        self.metric_layout.addLayout(self.mode_layout)
        self.thread_param_filter.start()
        self.thread_param_filter.image_update.connect(self.updateVideo)
        self.main_layout.addLayout(self.vidcap_layout)
        self.main_layout.addLayout(self.metric_layout)
        self.setLayout(self.main_layout)
        self.show()

    def updateVideo(self, img):
        self.vid_filter.setPixmap(QPixmap.fromImage(img))
    
    def update_method(self):    #0 -> methode Basique | 1 -> methode Moyenne | 2 -> methode Gaussienne
        self.data_access_controller.set_thresh_method(self.method_group.checkedId())

    def up_kernel(self):
        self.cent_val += 1
        if self.prev_id != self.button_group.checkedId() == 0:
            self.cent_val= 8
            self.prev_id= self.button_group.checkedId()

        if self.button_group.checkedId() == 0:
            self.data_access_controller.update_kernel(self.cent_val, "smooth")

        elif self.button_group.checkedId() == 1:
            self.data_access_controller.update_kernel(self.cent_val, "sharpen")

    def low_kernel(self):
        self.cent_val -= 1
        if self.prev_id != self.button_group.checkedId() == 0:
            self.cent_val= 8
            self.prev_id= self.button_group.checkedId()

        if self.button_group.checkedId() == 0:
            self.data_access_controller.update_kernel(self.cent_val, "smooth")

        elif self.button_group.checkedId() == 1:
            self.data_access_controller.update_kernel(self.cent_val, "sharpen")

    def update_all_params(self):
        if self.measure_unit.toPlainText() != "":
            if self.measure_unit.toPlainText().isnumeric():
                self.data_access_controller.set_ref_timer(int(self.measure_unit.toPlainText()))
        self.thread_param_filter.stop()
        self.hide()
        self.software_window= AnalyzerWindow(self.data_access_controller)
        self.software_window.show()

    def closeEvent(self, event):
        self.thread_param_filter.stop()

if __name__ == '__main__':
      
    # creating apyqt5 application
    app = QApplication(sys.argv)
    
    data_controller= DataAccessController()

    # creating a window object
    main = ParamsWindow(data_controller)
      
    # showing the window
    main.show()
  
    # loop
    sys.exit(app.exec_())

