#!/usr/bin/env python3
#
# WARNING: You should only use this approach for testing cscore on platforms that
#          it doesn't support using UsbCamera (Windows or OSX).
#

import cscore as cs
import time
from networktables import NetworkTable

import logging
logging.basicConfig(level=logging.DEBUG)

if hasattr(cs, 'UsbCamera'):
    camera = cs.UsbCamera("usbcam", 0)
    camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, 320, 240, 30)
else:
    import cv2
    import threading
    
    camera = cs.CvSource("cvsource", cs.VideoMode.PixelFormat.kMJPEG, 320, 240, 30)
    
    # tell OpenCV to capture video for us
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    
    # Do it in another thread
    def _thread():
        img = None
        while True:
            retval, img = cap.read(img)
            if retval:
                camera.putFrame(img)
        
    th = threading.Thread(target=_thread, daemon=True)
    th.start()

    # camera2 = cs.CvSource("cvsource", cs.VideoMode.PixelFormat.kMJPEG, 320, 240, 30)
    
    # # tell OpenCV to capture video for us
    # cap2 = cv2.VideoCapture(1)
    # cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    # cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    
    # # Do it in another thread
    # def _thread2():
    #     img2 = None
    #     while True:
    #         retval2, img2 = cap2.read(img2)
    #         if retval2:
    #             camera2.putFrame(img2)
        
    # th2 = threading.Thread(target=_thread2, daemon=True)
    # th2.start()
    

mjpegServer = cs.MjpegServer("httpserver", 8087)
mjpegServer.setSource(camera);

# mjpegServer2 = cs.MjpegServer("httpserver", 8086)
# mjpegServer2.setSource(camera2);


# NetworkTable.setClientMode()
# NetworkTable.setIPAddress('10.37.7.16')
# NetworkTable.initialize()

# time.sleep(5)

# smart = NetworkTable.getTable("CameraPublisher")
# cam = smart.getSubTable("RearCamera")

# cam.putString("source", "usb:IMAQdx/")
# cam.putStringArray("streams", ["mjpg:http://10.37.7.71:8087/stream.mjpg?name=Camera2"])

# cam2 = smart.getSubTable("FrontCamera")

# cam2.putString("source", "usb:IMAQdx/")
# cam2.putStringArray("streams", ["mjpg:http://10.37.7.71:8086/stream.mjpg?name=Camera2"])



print("mjpg server listening at http://0.0.0.0:8087")
input("Press enter to exit...")



# import cv2
# import numpy

# cv2.namedWindow("preview")
# vc = cv2.VideoCapture(0)

# if vc.isOpened(): # try to get the first frame
#     rval, frame = vc.read()
# else:
#     rval = False

# while rval:
#     # GripPipeline.process(vc)
#     cv2.imshow("preview", frame)
#     rval, frame = vc.read()
#     key = cv2.waitKey(20)
#     if key == 27: # exit on ESC
#         break
# cv2.destroyWindow("preview")