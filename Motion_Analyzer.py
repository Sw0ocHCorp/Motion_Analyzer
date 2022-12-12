import cv2 as cv
import numpy as np
import time
import math

CM_XY_1M= 165
REF_DZ= 1

isInit= False
cam_stream= cv.VideoCapture(0)
blur_coeff= 5
erode_iteration= 5
borne_min= 75
borne_max= 150
refContour= 0
kernel_1= np.array([[0, -1, 0], 
                    [-1, 8, -1], 
                    [0, -1, 0]])
big_contour= 0
peri_obj= 0
loc_memory= np.empty((0, 2), int)
speed_plot_data= np.empty((0,3), int)
acc_plot_data= np.empty((0,3), int)
plot3d_data= np.empty((0,3), int)
start_timer= time.perf_counter()
start_plot_timer= time.perf_counter()
x_motion= 0
y_motion= 0
angle= 0
time_second = -0.25
speed_plot_data= np.empty((0,3), int)
acc_plot_data= np.empty((0,3), int)
plot3d_data= np.empty((0,3), int)

def put_move_plot_data(motion_memory, speed_plot_data, acc_plot_data, plot3d_data, time_second, x_location, y_location):
        if (motion_memory.shape[0] > 2):
            max_index= motion_memory.shape[0] - 1
            x_speed=  int(motion_memory[max_index,0] - motion_memory[max_index-1,0]) *4
            y_speed= int(motion_memory[max_index,1] - motion_memory[max_index-1,1]) *4
            speed_plot_data= np.append(speed_plot_data, np.array([[time_second, x_speed, y_speed]]), axis= 0)
            print(speed_plot_data)
            if (speed_plot_data > 2):
                max_index_sp= speed_plot_data.shape[0] - 1
                x_acc= int(speed_plot_data[max_index_sp,1] - speed_plot_data[max_index_sp-1,1]) / 2
                y_acc= int(speed_plot_data[max_index_sp,2] - speed_plot_data[max_index_sp-1,2]) / 2
                acc_plot_data= np.append(acc_plot_data,np.array([[time_second, x_acc, y_acc]]), axis= 0)
            plot3d_data= np.append(plot3d_data,[x_location, 0, y_location], axis= 0)

def getMotionData(motion_memory, source_stream):
    motion= np.array([motion_memory[i+1, 0] - motion_memory[i, 0], motion_memory[i+1, 1] - motion_memory[i, 1]])
    prev_motion= np.array([motion_memory[i, 0] - motion_memory[i-1, 0], motion_memory[i, 1] - motion_memory[i-1, 1]])
    x_motion= np.abs(motion[0])
    y_motion= np.abs(motion[1])
    if motion_memory[i+1, 0] < motion_memory[i, 0]:
        if motion_memory[i+1, 1] < motion_memory[i, 1]:
            new_x_origin= int(motion_memory[i, 0])
            new_y_origin= int(motion_memory[i, 1])
            new_img_plan= source_stream[new_x_origin:, new_y_origin:]
        else:
            new_x_origin= int(motion_memory[i, 0])
            new_y_origin= int(motion_memory[i, 1])
            new_img_plan= source_stream[0:new_x_origin, new_y_origin:]
    else: 
        prev_motion= -prev_motion
        if motion_memory[i+1, 1] < motion_memory[i, 1]:
            new_x_origin= int(motion_memory[i, 0])
            new_y_origin= int(motion_memory[i, 1])
            new_img_plan= source_stream[new_x_origin:, new_y_origin:]
        else:
            new_x_origin= int(motion_memory[i, 0])
            new_y_origin= int(motion_memory[i, 1])
            new_img_plan= source_stream[0:new_x_origin, new_y_origin:]
    PI= 3.14159
    deg_angle= abs(math.atan2(motion[1], motion[0]) - math.atan2(prev_motion[1], prev_motion[0])) * (180 / PI)
        
    return x_motion, y_motion, deg_angle

while True:
    _, stream= cam_stream.read()
    stream_sh= cv.filter2D(stream, -1, kernel_1)
    stream_blur= cv.blur(stream, (blur_coeff, blur_coeff))
    stream_erode= cv.erode(stream_blur, None, iterations= erode_iteration)
    stream_gray= cv.cvtColor(stream_erode, cv.COLOR_BGR2GRAY)
    stream_sharp= cv.filter2D(stream_gray, -1, kernel_1)
    #_, thresh_stream= cv.threshold(stream_gray,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    _, thresh_stream= cv.threshold(stream_sharp,0,255, cv.THRESH_OTSU - cv.THRESH_BINARY)
    canny_stream= cv.Canny(thresh_stream, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #if isInit:
    contours, _= cv.findContours(canny_stream, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        big_contour= max(contours, key= cv.contourArea)                                     #On récupère le plus gros contour 
        x, y, w, h= cv.boundingRect(big_contour)
        bc_size= cv.contourArea(big_contour)
        if cv.contourArea(big_contour) > 50:
            loc_memory= np.append(loc_memory, np.array([[x+(w/2), y+(h/2)]]), axis= 0)
            if(loc_memory.shape[0]  > 10):
                loc_memory= np.delete(loc_memory, 0, 0)
            if (loc_memory.shape[0] > 2):
                for i in range(loc_memory.shape[0]-1):
                    x1= int(loc_memory[i, 0])
                    y1= int(loc_memory[i, 1])
                    x2= int(loc_memory[i+1, 0])
                    y2= int(loc_memory[i+1, 1])
                    cv.line(stream, (x1, y1), (x2, y2), (0, 0, 255-i*10), 3, 8)
                    end_timer= time.perf_counter()
                    if (end_timer - start_plot_timer) >= 0.25:
                            time_second += 0.25
                            matrix_test= put_move_plot_data(loc_memory, speed_plot_data, acc_plot_data, plot3d_data, time_second, x+(w/2), y+(h/2))
                            start_plot_timer= time.perf_counter()
                    if (end_timer - start_timer) >= 1:
                        start_timer= time.perf_counter()
                        x_motion, y_motion, angle= getMotionData(loc_memory, canny_stream)
                        #cv.putText(stream, "Distance Objet -> Camera= {:.2f}".format(refContoqqur / CM_XY_1M), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
            cv.rectangle(stream, (x, y), (x+w, y+h), (0, 255, 0), 2)                        #On trace le Rectangle correspondant
    cv.putText(stream, "Distance Objet -> X axis= {:.2f}, Y axis= {:.2f}, Angle= {:.2f}".format(x_motion, y_motion, angle), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv.imshow("User Stream", stream)
    cv.imshow("Sharp Stream", stream_sh)
    cv.imshow("TEST", canny_stream)

    if (cv.waitKey(1) & 0xFF) == ord("m"):
        isInit= True
        contours, _= cv.findContours(canny_stream, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            refContour= max(contours, key= cv.contourArea)                                     #On récupère le plus gros contour 
            peri_obj= cv.contourArea(refContour) / CM_XY_1M
            cv.putText(stream, "Périmètre de l'objet= {:.2f}".format(peri_obj), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

    if (cv.waitKey(1) & 0xFF) == ord("r"):
        loc_memory= np.empty((0, 2), int)
        pass

    if (cv.waitKey(1) & 0xFF) == ord("h"):
        refContour= 0

    if (cv.waitKey(1) & 0xFF) == ord("q"):
        cam_stream.release()
        cv.destroyAllWindows()
        break
