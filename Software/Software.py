import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from Windows_UI.AnalyzerWindow import AnalyzerWindow
from Windows_UI.ParamsWindow import ParamsWindow
from DataAccessController import DataAccessController

software= QApplication(sys.argv)
data_controller= DataAccessController()
setup_window = ParamsWindow(data_controller)
#software_window= AnalyzerWindow(data_controller)
setup_window.show()
#software_window.show()

sys.exit(software.exec_())