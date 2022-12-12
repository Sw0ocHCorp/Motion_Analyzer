import sys
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class PlotWindow(QWidget):
    def __init__(self):
        super(PlotWindow, self).__init__()
        self.fig= plt.figure()
        self.grid= GridSpec(4, 2, wspace=0.75, hspace=1)
        self.canva= FigureCanvasQTAgg(self.fig)
        self.toolbar = NavigationToolbar(self.canva, self)
        self.display_layout= QVBoxLayout()
        self.display_layout.addWidget(self.toolbar)
        self.display_layout.addWidget(self.canva)
        self.setLayout(self.display_layout)

    def plot_data(self, speedY_array, speedX_array, accelY_array, accelX_array, traj_array):
        self.fig.clear()
        self.ax_sY= self.fig.add_subplot(self.grid[0, 0])
        self.ax_sY.set_title("Evolution de la Vitesse (Axe Y)")
        self.ax_sY.set_xlabel("Temps")
        self.ax_sY.set_ylabel("pxs")
        self.ax_sY.plot(speedY_array)
        self.ax_sX= self.fig.add_subplot(self.grid[0, 1])
        self.ax_sX.set_title("Evolution de la Vitesse (Axe X)")
        self.ax_sX.set_xlabel("Temps")
        self.ax_sX.set_ylabel("pxs")
        self.ax_sX.plot(speedX_array)
        self.ax_aY= self.fig.add_subplot(self.grid[1, 0])
        self.ax_aY.set_title("Evolution de l'Accélération' (Axe Y)")
        self.ax_aY.set_xlabel("Temps")
        self.ax_aY.set_ylabel("pxs")
        self.ax_aY.plot(accelY_array)
        self.ax_aX= self.fig.add_subplot(self.grid[1, 1])
        self.ax_aX.set_title("Evolution de l'Accélération (Axe X)")
        self.ax_aX.set_xlabel("Temps")
        self.ax_aX.set_ylabel("pxs")
        self.ax_aX.plot(accelX_array)
        self.ax_traj= self.fig.add_subplot(self.grid[2:3, :], projection='3d')
        self.ax_traj.set_title("Trajectoire de l'Objet")
        self.ax_traj.set_xlabel("Position latérale (px)")
        self.ax_traj.set_ylabel("Distance par rapport à la Caméra (px)")
        self.ax_traj.set_zlabel("Position verticale (px)")
        self.ax_traj.plot(traj_array[:,0], traj_array[:,1], traj_array[:,2], color='red', lw=7)
        self.canva.draw()

if __name__ == '__main__':
      
    # creating apyqt5 application
    app = QApplication(sys.argv)
  
    # creating a window object
    main = PlotWindow()
    main.plot_data(np.array([0, 1]), np.array([0, 1]), np.array([0, 1]), np.array([0, 1]), np.array([[0, 0, 0],
                                                                                                    [100, 50, 50],
                                                                                                    [100, 100, 0]]))  
      
    # showing the window
    main.show()
  
    # loop
    sys.exit(app.exec_())