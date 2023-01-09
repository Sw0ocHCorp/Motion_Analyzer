import sys
sys.path.insert(0, "C:\\Users\\nclsr\\OneDrive\\Bureau\\Projets_FabLab_IA\\Motion_Analyzer\\Software")
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Thread_Software.ThreadFilterView import ThreadFilterView
from DataAccessController import DataAccessController
from Windows_UI.AnalyzerWindow import AnalyzerWindow
import numpy as np

# --> Classe représentant la fenêtre de paramétrage
class ParamsWindow(QWidget):
    def __init__(self, data_access_controller):                 # --* Constructeur: Définition des objets affichés dans la fenêtre
        super().__init__()
        self.data_access_controller= data_access_controller
        self.cent_val= 8
        self.kernel= np.array(  [[0, -1, 0], 
                                     [-1, self.cent_val, -1], 
                                     [0, -1, 0]])
        self.prev_id= 1

        self.main_layout= QVBoxLayout()
        self.button_layout= QHBoxLayout()
        self.rad_button_layout= QHBoxLayout()
        self.vidcap_layout= QHBoxLayout()
        self.metric_layout= QVBoxLayout()
        self.mode_layout= QVBoxLayout()
        self.thresh_layout= QVBoxLayout()
        self.thresh_layout.setContentsMargins(0, 15, 0, 15)
        self.vid_cam= QLabel()
        self.vid_filter= QLabel()
        self.vid_usb= QLabel()
        self.vid_usb_filter= QLabel()
        self.vid_cam_layout= QStackedLayout()
        self.vid_filter_layout= QStackedLayout()
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
        self.mode_cam= QCheckBox("Activer le mode Duo Cam")
        self.mode_cam.setChecked(False)
        self.mode_cam.stateChanged.connect(self.select_mode_cam)
        self.thresh_basic.setChecked(True)
        self.method_group.addButton(self.thresh_basic, 0)
        self.method_group.addButton(self.thresh_mean, 1)
        self.method_group.addButton(self.thresh_gaussian, 2)
        self.method_group.buttonClicked.connect(self.update_method)
        self.more_button.clicked.connect(self.up_kernel)
        self.less_button.clicked.connect(self.low_kernel)
        self.valid_button.clicked.connect(self.update_all_params)
        self.setWindowTitle("Params")
        self.setFixedSize(1920, 1000)
        self.thread_param_filter= ThreadFilterView(data_access_controller, 0)
        self.usb_vid_thread= ThreadFilterView(self.data_access_controller, 1)
        self.metric_layout.addWidget(QLabel("Choisissez l'unité de références \npour le Calcul de Vitesse / Accélération (en ms)"))
        self.metric_layout.addWidget(self.measure_unit)
        self.metric_layout.addWidget(self.mode_cam)
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
        self.metric_layout.addLayout(self.mode_layout)
        self.thread_param_filter.start()
        self.thread_param_filter.vid_cam.connect(self.update_vid_cam)
        self.thread_param_filter.vid_filter.connect(self.update_vid_filter)
        self.usb_vid_thread.vid_cam.connect(self.update_vid_usb)
        self.usb_vid_thread.vid_filter.connect(self.update_vid_usb_filter)
        

        self.vidcap_layout.addWidget(self.vid_cam)
        self.vidcap_layout.addWidget(self.vid_filter)
        self.main_layout.addLayout(self.vidcap_layout)
        self.main_layout.addLayout(self.metric_layout)
        self.setLayout(self.main_layout)
        self.show()

    def select_mode_cam(self, state):                               # --* Méthode appelé lors du changement d'état de la checkbox: Choix du mode Duo Cam
        if state != self.mode_cam.isChecked():
            print("Duo Cam Enable")
            self.data_access_controller.set_Duo_Cam(True)
            for i in range(self.vidcap_layout.count()):
                self.vidcap_layout.itemAt(i).widget().close()
            item = self.main_layout.itemAt(0)
            widget = item.layout()
            widget.deleteLater()
            self.vidcap_layout= QHBoxLayout()
            self.vid_cam= QLabel()
            self.vid_filter= QLabel()
            self.vid_usb= QLabel()
            self.vid_usb_filter= QLabel()
            self.vidcap_layout.addWidget(self.vid_cam)
            self.vidcap_layout.addWidget(self.vid_filter)
            self.vidcap_layout.addWidget(self.vid_usb)
            self.vidcap_layout.addWidget(self.vid_usb_filter)
            self.main_layout.insertLayout(0, self.vidcap_layout)
            self.usb_vid_thread.start()
        else:
            print("Duo Cam Disable")
            self.data_access_controller.set_Duo_Cam(False)
            self.vidcap_layout.itemAt(2).widget().close()
            self.vidcap_layout.itemAt(3).widget().close()

    def update_vid_cam(self, img):                              # --* Méthode permettant d'incruster la vidéo dans l'interface
        self.vid_cam.setPixmap(QPixmap.fromImage(img))
    
    def update_vid_filter(self, img):                           # --* Méthode permettant d'incruster la vidéo dans l'interface
        self.vid_filter.setPixmap(QPixmap.fromImage(img))
    
    def update_vid_usb(self, img):                              # --* Méthode permettant d'incruster la vidéo dans l'interface
        self.vid_usb.setPixmap(QPixmap.fromImage(img))
    
    def update_vid_usb_filter(self, img):                       # --* Méthode permettant d'incruster la vidéo dans l'interface
        self.vid_usb_filter.setPixmap(QPixmap.fromImage(img))
    
    def update_method(self):                                    # --* Méthode appelée lors du changement de bouton sélectionné du groupe de radioButton: Choix du mode de détection des contours
        self.data_access_controller.set_thresh_method(self.method_group.checkedId())

    def up_kernel(self):                                        # --* Méthode appelée sur le bouton "Accentuer": Accentue le filtrage sélectionné
        self.cent_val += 1
        if self.prev_id != self.button_group.checkedId() == 0:
            self.cent_val= 8
            self.prev_id= self.button_group.checkedId()

        if self.button_group.checkedId() == 0:
            self.data_access_controller.update_kernel(self.cent_val, "smooth")

        elif self.button_group.checkedId() == 1:
            self.data_access_controller.update_kernel(self.cent_val, "sharpen")

    def low_kernel(self):                                       # --* Méthode appelée sur le bouton "Réduire": Diminue le filtrage sélectionné
        self.cent_val -= 1
        if self.prev_id != self.button_group.checkedId() == 0:
            self.cent_val= 8
            self.prev_id= self.button_group.checkedId()

        if self.button_group.checkedId() == 0:
            self.data_access_controller.update_kernel(self.cent_val, "smooth")

        elif self.button_group.checkedId() == 1:
            self.data_access_controller.update_kernel(self.cent_val, "sharpen")

    def update_all_params(self):                                # --* Méthode appelée sur le bouton "Valider": Sauvegarde de tous les paramêtres sélectionnés
        if self.measure_unit.toPlainText() != "":
            if self.measure_unit.toPlainText().isnumeric():
                self.data_access_controller.set_ref_timer(int(self.measure_unit.toPlainText()))
        self.thread_param_filter.stop()
        self.usb_vid_thread.stop()
        self.data_access_controller.adapt_cam_number()
        self.close()
        
        self.software_window= AnalyzerWindow(self.data_access_controller)

    def closeEvent(self, event):
        self.thread_param_filter.stop()
        self.usb_vid_thread.stop()

if __name__ == '__main__':                          # TEST INDéPENDANT DE L'INTERFACE
      
    # creating apyqt5 application
    app = QApplication(sys.argv)
    
    data_controller= DataAccessController()

    # creating a window object
    main = ParamsWindow(data_controller)
      
    # showing the window
    main.show()
  
    # loop
    sys.exit(app.exec_())

