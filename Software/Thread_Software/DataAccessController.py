from threading import Semaphore
import numpy as np

class DataAccessController():
    def __init__(self):
        self.gateway= Semaphore()
        self.motion_memory= np.empty((0,2), int)
        self.x_motion= self.y_motion= self.deg_angle= 0
    
    def put_localisation_data(self, object_localisation):
        self.motion_memory= np.append(self.motion_memory, object_localisation, axis= 0)

    def get_motion_memory(self):
        if(self.motion_memory.shape[0]  > 10):
            self.motion_memory= np.delete(self.motion_memory, 0, 0)
        return self.motion_memory
    
    def put_motion_data(self, x_motion, y_motion, deg_angle):
        self.x_motion= x_motion
        self.y_motion= y_motion
        self.deg_angle= deg_angle

    def get_motion_data(self):
        return self.x_motion, self.y_motion, self.deg_angle

    def enable_data_access(self):
        self.gateway.acquire()

    def disable_data_access(self):
        self.gateway.release()
    
    def data_access_is_enable(self, timeout= 1):
        return self.gateway.acquire(blocking= True, timeout= timeout)