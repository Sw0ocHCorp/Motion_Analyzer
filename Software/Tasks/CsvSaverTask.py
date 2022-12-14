import csv
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class CsvSaverTask(QThread):
    def __init__(self, data_controller):
        super().__init__()
        self. data_controller = data_controller
        self.filename = "debug.csv"
        self.delimiter = ";"
        self.prev_time= -1
        self.csv_file= open(self.filename, 'a', newline= "")
        self.writer = csv.writer(self.csv_file, delimiter= self.delimiter)
        self.writer.writerow(["TEMPS (seconde)", "Vitesse axe X (pxs/s)", "Vitesse axe Y (pxs/s)", "Acceleration axe X (pxs/s)", "Acceleration axe Y (pxs/s)"])


    def do_task(self):
        if self.writer == None:
            self.writer = csv.writer(self.csv_file, delimiter= self.delimiter)
        #self.data_controller.enable_data_access()
        self.speed_plot_data, self.acc_plot_data, self.plot3d_data= self.data_controller.get_motion_plot_data()
        #self.data_controller.disable_data_access()
        if self.speed_plot_data.shape[0] > 0:
            self.time= self.speed_plot_data[-1,0]
            if self.time > self.prev_time:
                print(self.time)
                self.prev_time= self.time
                self.speed_x= self.speed_plot_data[-1,1]
                self.speed_y= self.speed_plot_data[-1,2]
                if self.acc_plot_data.shape[0] > 0:
                    self.acc_x= self.acc_plot_data[-1,1]
                    self.acc_y= self.acc_plot_data[-1,2]
                    try:
                        self.writer.writerow([self.time, self.speed_x, self.speed_y, self.acc_x, self.acc_y])
                    except:
                        print("Error writing to CSV file")

    def end_task(self):
        print("-----> END CSV FILE")
        self.csv_file.close()
        self.writer = None