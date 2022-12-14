from threading import Semaphore
import numpy as np

class DataAccessController():
    def __init__(self):
        self.gateway= Semaphore()
        self.stream_gateway= Semaphore()
        self.motion_memory= np.empty((0,2), int)
        self.speed_plot_data= np.empty((0,3), int)
        self.acc_plot_data= np.empty((0,3), int)
        self.plot3d_data= np.empty((0,3), int)
        self.x_motion= self.y_motion= self.deg_angle= 0

    def get_motion_memory(self):
        if(self.motion_memory.shape[0]  > 10):
            self.motion_memory= np.delete(self.motion_memory, 0, 0)
        return self.motion_memory

    def update_motion_memory(self, object_localisation):
        self.motion_memory= np.append(self.motion_memory, object_localisation, axis= 0)
        if(self.motion_memory.shape[0]  > 10):
            self.motion_memory= np.delete(self.motion_memory, 0, 0)
        return self.motion_memory
    
    def put_move_plot_data(self, time_second, x_location, y_location):
        if (self.motion_memory.shape[0] > 2):
            max_index= self.motion_memory.shape[0] - 1
            self.x_speed=  int(self.motion_memory[max_index,0] - self.motion_memory[max_index-1,0]) *4
            self.y_speed= int(self.motion_memory[max_index,1] - self.motion_memory[max_index-1,1]) *4
            self.speed_plot_data= np.append(self.speed_plot_data,np.array([[time_second, self.x_speed, self.y_speed]]), axis= 0)
            if (self.speed_plot_data.shape[0] > 2):
                max_index_sp= self.speed_plot_data.shape[0] - 1
                self.x_acc= int(self.speed_plot_data[max_index_sp,1] - self.speed_plot_data[max_index_sp-1,1]) / 2
                self.y_acc= int(self.speed_plot_data[max_index_sp,2] - self.speed_plot_data[max_index_sp-1,2]) / 2
                self.acc_plot_data= np.append(self.acc_plot_data,np.array([[time_second, self.x_acc, self.y_acc]]), axis= 0)
                #print(time_second, self.x_speed, self.y_speed, self.x_acc, self.y_acc)
            self.plot3d_data= np.append(self.plot3d_data,np.array([[x_location, 0, y_location]]), axis= 0)

    def get_motion_plot_data(self):
        return self.speed_plot_data, self.acc_plot_data, self.plot3d_data

    def put_motion_data(self, x_motion, y_motion, deg_angle):
        self.x_motion= x_motion
        self.y_motion= y_motion
        self.deg_angle= deg_angle

    def put_stream(self, stream):
        self.stream= stream

    def get_stream(self):
        return self.stream

    def get_motion_data(self):
        return self.x_motion, self.y_motion, self.deg_angle

    def enable_data_access(self):
        self.gateway.acquire()

    def disable_data_access(self):
        self.gateway.release()
    
    def data_access_is_enable_timeout(self, timeout= 1):
        return self.gateway.acquire(blocking= True, timeout= timeout)
    
    def enable_stream_access(self):
        self.stream_gateway.acquire()

    def disable_stream_access(self):
        self.stream_gateway.release()
    
    def stream_access_is_enable(self):
        isEnable= False
        if self.stream_gateway._value >= 0:
            isEnable= True
        return isEnable
    
    def stream_access_is_enable_timeout(self, timeout= 1):
        return self.stream_gateway.acquire(blocking= True, timeout= timeout)

    def reset_data(self):
        self.motion_memory= np.empty((0,2), int)
        self.motion_plot_data= np.empty((0,3), int)
        self.x_motion= self.y_motion= self.deg_angle= 0