import sys
import numpy as np
import time
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# --> Classe permettant de représenter la tâche de tracé des données sur les graphiques
class PlotDataTask(QThread):
    def __init__(self, plot_window, data_controller):
        super().__init__()
        self.plot_window= plot_window
        self.data_controller= data_controller
        self.isDuoCam= self.data_controller.get_Duo_Cam()
        
    def do_task(self):                                  # --* Méthode de la tâche appelée par le Pattern Observer
        self.start()
        
    def run(self):                                      # --* Méthode d'affichage des données sur les graphiques || Méthode appelée par la méthode start() de la classe QThread
        #self.data_controller.enable_data_access()
        self.speed_plot_data, self.acc_plot_data, self.plot3d_data= self.data_controller.get_motion_plot_data()
        #self.data_controller.disable_data_access()
        speed_y= np.column_stack((self.speed_plot_data[:,0], self.speed_plot_data[:,2]))
        speed_x= np.column_stack((self.speed_plot_data[:,0], self.speed_plot_data[:,1]))
        acc_y= np.column_stack((self.acc_plot_data[:,0], self.acc_plot_data[:,2]))
        acc_x= np.column_stack((self.acc_plot_data[:,0], self.acc_plot_data[:,1]))
        if self.isDuoCam == True:
            speed_z= np.column_stack((self.speed_plot_data[:,0], self.speed_plot_data[:,3]))
            acc_z= np.column_stack((self.acc_plot_data[:,0], self.acc_plot_data[:,3]))
            self.plot_window.plot_full_data(speed_y, speed_x, speed_z, acc_y, acc_x, acc_z, self.plot3d_data)
        else:
            self.plot_window.plot_data(speed_y, speed_x, acc_y, acc_x, self.plot3d_data)