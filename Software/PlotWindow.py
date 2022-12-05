import sys
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np

class PlotWindow(QWidget):
    def __init__(self):
        super(PlotWindow, self).__init__()
        self.fig, self.axs= plt.subplots(2)
        self.canva= FigureCanvasQTAgg(self.fig)
        self.toolbar = NavigationToolbar(self.canva, self)
        self.display_layout= QVBoxLayout()
        self.display_layout.addWidget(self.toolbar)
        self.display_layout.addWidget(self.canva)
        self.setLayout(self.display_layout)

    def plot_data(self, speed_array, accel_array):
        self.fig.clear()
        self.axs= self.fig.subplots(2)
        self.axs[0].plot(speed_array)
        #self.axs[0].set_title("Evolution de la Vitesse")
        #self.axs[0].set_xlabel("Temps")
        #self.axs[0].set_ylabel("px/s")
        self.axs[1].plot(accel_array)
        #self.axs[1].set_title("Evolution de l'Acceleration")
        #self.axs[1].set_xlabel("Temps")
        #self.axs[1].set_ylabel("px/s")
        self.canva.draw()

if __name__ == '__main__':
      
    # creating apyqt5 application
    app = QApplication(sys.argv)
  
    # creating a window object
    main = PlotWindow()
    main.plot_data(np.array([0, 1]), np.array([0, 1]))  
      
    # showing the window
    main.show()
  
    # loop
    sys.exit(app.exec_())