import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from Windows_UI.AnalyzerWindow import AnalyzerWindow

software= QApplication(sys.argv)
software_window= AnalyzerWindow()
software_window.show()

sys.exit(software.exec_())