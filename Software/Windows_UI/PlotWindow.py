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

# --> Classe permettant de représenter l'objet graphique affichant les graphiques
class PlotWindow(QWidget):
    def __init__(self):                                # --* Constructeur: Définition du design de l'objet graphique
        super(PlotWindow, self).__init__()
        self.fig_2D= plt.figure()
        self.fig_3D= plt.figure()
        self.grid= GridSpec(2, 3, wspace=0.75, hspace=1)
        self.canva_2D= FigureCanvasQTAgg(self.fig_2D)
        self.canva_3D= FigureCanvasQTAgg(self.fig_3D)
        self.display_layout= QVBoxLayout()
        self.display_layout.addWidget(self.canva_2D)
        self.display_layout.addWidget(self.canva_3D)
        self.setLayout(self.display_layout)
    
    def plot_full_data(self, speedY_array, speedX_array, speedZ_array, accelY_array, accelX_array, accelZ_array, traj_array):   # --* Méthode de sélection de la fenêtre en Mode DuoCam
        self.fig_2D.clear()
        self.fig_3D.clear()
        self.fig_3D.subplots_adjust(left=0, right=1, bottom=0, top=1)
        self.ax_sY= self.fig_2D.add_subplot(self.grid[0, 0])
        self.ax_sY.set_title("Evolution de la Vitesse (Axe Y)")
        self.ax_sY.set_xlabel("Temps")
        self.ax_sY.set_ylabel("pxs")
        self.ax_sY.plot(speedY_array)
        self.ax_sX= self.fig_2D.add_subplot(self.grid[0, 1])
        self.ax_sX.set_title("Evolution de la Vitesse (Axe X)")
        self.ax_sX.set_xlabel("Temps")
        self.ax_sX.set_ylabel("pxs")
        self.ax_sX.plot(speedX_array)
        self.ax_sZ= self.fig_2D.add_subplot(self.grid[0, 2])
        self.ax_sZ.set_title("Evolution de la Vitesse (Axe X SideCam / Axe Z MainCam)")
        self.ax_sZ.set_xlabel("Temps")
        self.ax_sZ.set_ylabel("pxs")
        self.ax_sZ.plot(speedZ_array)

        self.ax_aY= self.fig_2D.add_subplot(self.grid[1, 0])
        self.ax_aY.set_title("Evolution de l'Accélération' (Axe Y)")
        self.ax_aY.set_xlabel("Temps")
        self.ax_aY.set_ylabel("pxs")
        self.ax_aY.plot(accelY_array)
        self.ax_aX= self.fig_2D.add_subplot(self.grid[1, 1])
        self.ax_aX.set_title("Evolution de l'Accélération (Axe X)")
        self.ax_aX.set_xlabel("Temps")
        self.ax_aX.set_ylabel("pxs")
        self.ax_aX.plot(accelX_array)
        self.ax_aZ= self.fig_2D.add_subplot(self.grid[1, 2])
        self.ax_aZ.set_title("Evolution de l'Accélération (Axe X SideCam / Axe Z MainCam)")
        self.ax_aZ.set_xlabel("Temps")
        self.ax_aZ.set_ylabel("pxs")
        self.ax_aZ.plot(accelZ_array)

        self.ax_traj= self.fig_3D.add_subplot(projection='3d')
        self.ax_traj.set_title("Trajectoire de l'Objet")
        self.ax_traj.set_xlabel("Position latérale (px)")
        self.ax_traj.set_ylabel("Distance par rapport à la Caméra (px)")
        self.ax_traj.set_zlabel("Position verticale (px)")
        self.ax_traj.plot(traj_array[:,0], traj_array[:,1], traj_array[:,2], color='red', lw=7)
        self.canva_2D.draw()
        self.canva_3D.draw()

    def plot_data(self, speedY_array, speedX_array, accelY_array, accelX_array, traj_array):        # --* Méthode de sélection de la fenêtre en Mode Caméra Simple
        self.fig_2D.clear()
        self.fig_3D.clear()
        self.fig_3D.subplots_adjust(left=0, right=1, bottom=0, top=1)
        self.ax_sY= self.fig_2D.add_subplot(self.grid[0, 0])
        self.ax_sY.set_title("Evolution de la Vitesse (Axe Y)")
        self.ax_sY.set_xlabel("Temps")
        self.ax_sY.set_ylabel("pxs")
        self.ax_sY.plot(speedY_array)
        self.ax_sX= self.fig_2D.add_subplot(self.grid[0, 1])
        self.ax_sX.set_title("Evolution de la Vitesse (Axe X)")
        self.ax_sX.set_xlabel("Temps")
        self.ax_sX.set_ylabel("pxs")
        self.ax_sX.plot(speedX_array)
        self.ax_aY= self.fig_2D.add_subplot(self.grid[1, 0])
        self.ax_aY.set_title("Evolution de l'Accélération' (Axe Y)")
        self.ax_aY.set_xlabel("Temps")
        self.ax_aY.set_ylabel("pxs")
        self.ax_aY.plot(accelY_array)
        self.ax_aX= self.fig_2D.add_subplot(self.grid[1, 1])
        self.ax_aX.set_title("Evolution de l'Accélération (Axe X)")
        self.ax_aX.set_xlabel("Temps")
        self.ax_aX.set_ylabel("pxs")
        self.ax_aX.plot(accelX_array)
        self.ax_traj= self.fig_3D.add_subplot(projection='3d')
        self.ax_traj.set_title("Trajectoire de l'Objet")
        self.ax_traj.set_xlabel("Position latérale (px)")
        self.ax_traj.set_ylabel("Distance par rapport à la Caméra (px)")
        self.ax_traj.set_zlabel("Position verticale (px)")
        self.ax_traj.plot(traj_array[:,0], traj_array[:,1], traj_array[:,2], color='red', lw=7)
        self.canva_2D.draw()
        self.canva_3D.draw()

if __name__ == '__main__':          #TEST INDéPENDANT DE L'OBJET GRAPHIQUE
      
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