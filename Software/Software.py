import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from AnalyzerWindow import AnalyzerWindow

software= QApplication(sys.argv)
software_window= AnalyzerWindow()
software_window.show()

software.exec_()