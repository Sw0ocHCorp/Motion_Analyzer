from threading import Semaphore
import numpy as np

# --> Classe Modélisant le contrôleur d'accès aux données || Banque de données commun à chaques classes
class DataAccessController():
    def __init__(self):
        self.gateway= Semaphore()
        self.stream_gateway= Semaphore()
        self.motion_memory= np.empty((0,2), int)
        self.duo_motion_memory= np.empty((0,2), int)
        self.speed_plot_data= np.empty((0,4), int)
        self.acc_plot_data= np.empty((0,4), int)
        self.plot3d_data= np.empty((0,3), int)
        self.duo_speed_data= np.empty((0,2), int)
        self.duo_acc_data= np.empty((0,2), int)

        self.x_motion= self.y_motion= self.deg_angle= 0
        self.z_speed= self.z_acc= 0
        self.detection= False
        self.kernel= np.array([[0, -1, 0], 
                                 [-1, 8, -1], 
                                 [0, -1, 0]])
        self.ref_timer= 0.25
        self.thresh_mode= 0
        self.isDuoCam= False
        self.streams_bank= np.array([], dtype= object)

    def update_kernel(self, cent_val, mode):                    # --* Méthode permettant de mettre à jour le noyau de convolution pour le Filtrage
        if mode == "sharpen":
            self.kernel= np.array([[0, -1, 0], 
                                    [-1, cent_val, -1], 
                                    [0, -1, 0]])
        elif mode == "smooth":
            self.kernel= np.array([[0, 1, 0], 
                                    [1, cent_val, 1], 
                                    [0, 1, 0]])
    
    def adapt_cam_number(self):                                 #--* Méthode d'adaptation de la forme des matrices de données (Vitesse / Accélération) en fonction du nombre de caméras
        if self.isDuoCam:
            self.speed_plot_data= np.empty((0,4), int)
            self.acc_plot_data= np.empty((0,4), int)
        else:
            self.speed_plot_data= np.empty((0,3), int)
            self.acc_plot_data= np.empty((0,3), int)

    def get_kernel(self):
        return self.kernel

    def set_ref_timer(self, ref_timer= 1000):                   # --* Méthode permettant de mettre à jour le l'intervalle de temps entre 2 prises de mesures
        self.ref_timer= ref_timer / 1000

    def get_ref_timer(self):
        return self.ref_timer

    def set_thresh_method(self, method_id):
            self.thresh_mode= method_id
    
    def get_thresh_method(self):
        return self.thresh_mode

    def update_motion_memory(self, object_localisation, isMain):                                # --* Méthode permettant de mettre à jour la mémoire de déplacement
        if isMain:
            self.motion_memory= np.append(self.motion_memory, object_localisation, axis= 0)
            if(self.motion_memory.shape[0]  > 10):
                self.motion_memory= np.delete(self.motion_memory, 0, 0)
            return self.motion_memory
        else:
            self.z_localisation= object_localisation[0, 0]
            self.duo_motion_memory= np.append(self.duo_motion_memory, object_localisation, axis= 0)
            if(self.duo_motion_memory.shape[0]  > 10):
                self.duo_motion_memory= np.delete(self.duo_motion_memory, 0, 0)
            return self.duo_motion_memory

    def put_move_plot_data(self, time_second, x_location, y_location, isMain):                  # --* Méthode permettant de mettre à jour les données de déplacement pour chaques graphiques
        if isMain:
            if (self.motion_memory.shape[0] > 2):
                max_index= self.motion_memory.shape[0] - 1
                if self.ref_timer < 1:
                    self.x_speed=  int(self.motion_memory[max_index,0] - self.motion_memory[max_index-1,0]) * (1/self.ref_timer)
                    self.y_speed= int(self.motion_memory[max_index,1] - self.motion_memory[max_index-1,1]) * (1/self.ref_timer)
                else:
                    self.x_speed=  int(self.motion_memory[max_index,0] - self.motion_memory[max_index-1,0]) / self.ref_timer
                    self.y_speed= int(self.motion_memory[max_index,1] - self.motion_memory[max_index-1,1]) / self.ref_timer
                if self.isDuoCam:
                    self.speed_plot_data= np.append(self.speed_plot_data,np.array([[time_second, self.x_speed, self.y_speed, self.z_speed]]), axis= 0)
                else:
                    self.speed_plot_data= np.append(self.speed_plot_data,np.array([[time_second, self.x_speed, self.y_speed]]), axis= 0)
                if (self.speed_plot_data.shape[0] > 2):
                    max_index_sp= self.speed_plot_data.shape[0] - 1
                    self.x_acc= int(self.speed_plot_data[max_index_sp,1] - self.speed_plot_data[max_index_sp-1,1]) / 2
                    self.y_acc= int(self.speed_plot_data[max_index_sp,2] - self.speed_plot_data[max_index_sp-1,2]) / 2
                    if self.isDuoCam:
                        self.acc_plot_data= np.append(self.acc_plot_data,np.array([[time_second, self.x_acc, self.y_acc, self.z_acc]]), axis= 0)
                    else:
                        self.acc_plot_data= np.append(self.acc_plot_data,np.array([[time_second, self.x_acc, self.y_acc]]), axis= 0)
                #print(time_second, self.x_speed, self.y_speed, self.x_acc, self.y_acc)
                if self.isDuoCam:
                    self.plot3d_data= np.append(self.plot3d_data,np.array([[x_location, self.z_localisation, y_location]]), axis= 0)
                else:
                    self.plot3d_data= np.append(self.plot3d_data,np.array([[x_location, 0, y_location]]), axis= 0)
        else:
            if (self.duo_motion_memory.shape[0] > 2):
                max_index= self.duo_motion_memory.shape[0] - 1
                if self.ref_timer < 1:
                    self.z_speed=  int(self.duo_motion_memory[max_index,0] - self.duo_motion_memory[max_index-1,0]) * (1/self.ref_timer)
                else:
                    self.z_speed=  int(self.duo_motion_memory[max_index,0] - self.duo_motion_memory[max_index-1,0]) / self.ref_timer
                self.duo_speed_data= np.append(self.duo_speed_data,np.array([[time_second, self.z_speed]]), axis= 0)
                if (self.duo_speed_data.shape[0] > 2):
                    max_index_sp= self.duo_speed_data.shape[0] - 1
                    self.z_acc= int(self.duo_speed_data[max_index_sp,1] - self.duo_speed_data[max_index_sp-1,1]) / 2
                    self.duo_acc_data= np.append(self.duo_acc_data,np.array([[time_second, self.z_acc]]), axis= 0)

    def get_motion_plot_data(self):                                         # --* Getter permettant d'afficher les données sur chaques graphiques
        return self.speed_plot_data, self.acc_plot_data, self.plot3d_data

    def reset_data(self):                                                   # --* Méthode permettant de réinitialiser les données de déplacement
        self.motion_memory= np.empty((0,2), int)
        self.duo_motion_memory= np.empty((0,2), int)

    def get_Duo_Cam(self):
        return self.isDuoCam

    def set_Duo_Cam(self, isDuoCam):
        self.isDuoCam= isDuoCam