import cv2 as cv
import numpy as np

# PROGRAMME DE TEST DE LA DOUBLE DIFFUSION
initCam= False
cam_pc= cv.VideoCapture(0)
cam_usb= cv.VideoCapture(1)
kernel_1= np.array([[0, -1, 0], 
                    [-1, 8, -1], 
                    [0, -1, 0]])

while True:
    print(cam_usb.isOpened())
    print(cam_pc.isOpened())
    if initCam == False:
        initCam= True
        if cam_usb.isOpened() == True & cam_pc.isOpened() == True:
            cam_pc= cv.VideoCapture(1)
            cam_usb= cv.VideoCapture(0)
    _, pc_stream= cam_pc.read()
    #_, usb_stream= cam_usb.read()
    #cv.imshow("CAM Stream", usb_stream)
    cv.imshow("PC Stream", pc_stream)
    """stream_sh= cv.filter2D(pc_stream, -1, kernel_1)
    stream_blur= cv.blur(pc_stream, (3, 3))
    stream_erode= cv.erode(stream_blur, None, iterations= 2)
    stream_gray= cv.cvtColor(stream_erode, cv.COLOR_BGR2GRAY)
    stream_sharp= cv.filter2D(stream_gray, -1, kernel_1)
    _, thresh_stream= cv.threshold(stream_gray,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    _, thresh_stream= cv.threshold(stream_sharp,0,255, cv.THRESH_OTSU - cv.THRESH_BINARY)
    canny_stream= cv.Canny(thresh_stream, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cv.imshow("User Stream", pc_stream)
    cv.imshow("Sharp Stream", stream_sh)
    cv.imshow("TEST", canny_stream)"""

    if (cv.waitKey(1) & 0xFF) == ord("q"):
        cam_pc.release()
        #cam_usb.release()
        cv.destroyAllWindows()
        break