import sys
import numpy as np
import time
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class PlotDataTask():
    def __init__(self, plot_window):
        self.plot_window= plot_window
        
    def do_task(self):
        self.plot_window.plot_data(np.array([0, 1]), np.array([0, 1]), np.array([0, 1]), np.array([0, 1]), np.array([[0, 0, 0],
                                                                                                                    [10, 5, 5],
                                                                                                                    [10, 10, 0]]))