import sys
import numpy as np
import time
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class PlotDataTask(QThread):
    def __init__(self, plot_window, data_controller):
        super().__init__()
        self.plot_window= plot_window
        self.data_controller= data_controller
        
    def do_task(self):
        self.start()
    def run(self):
        self.data_controller.enable_data_access()
        self.speed_plot_data, self.acc_plot_data, self.plot3d_data= self.data_controller.get_motion_plot_data()
        self.data_controller.disable_data_access()
        speed_y= np.column_stack((self.speed_plot_data[:,0], self.speed_plot_data[:,2]))
        speed_x= np.column_stack((self.speed_plot_data[:,0], self.speed_plot_data[:,1]))
        acc_y= np.column_stack((self.acc_plot_data[:,0], self.acc_plot_data[:,2]))
        acc_x= np.column_stack((self.acc_plot_data[:,0], self.acc_plot_data[:,1]))
        self.plot_window.plot_data(speed_y, speed_x, acc_y, acc_x, self.plot3d_data)