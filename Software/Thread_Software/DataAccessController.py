from threading import Semaphore
import numpy as np

class DataAccessController():
    def __init__(self):
        self.gateway= Semaphore()
        self.stream_gateway= Semaphore()
        self.motion_memory= np.empty((0,2), int)
        self.x_motion= self.y_motion= self.deg_angle= 0
    
    def put_localisation_data(self, object_localisation):
        self.motion_memory= np.append(self.motion_memory, object_localisation, axis= 0)

    def get_motion_memory(self):
        if(self.motion_memory.shape[0]  > 10):
            self.motion_memory= np.delete(self.motion_memory, 0, 0)
        return self.motion_memory

    def update_motion_memory(self, object_localisation):
        self.motion_memory= np.append(self.motion_memory, object_localisation, axis= 0)
        if(self.motion_memory.shape[0]  > 10):
            self.motion_memory= np.delete(self.motion_memory, 0, 0)
        return self.motion_memory
    
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