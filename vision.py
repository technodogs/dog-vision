import time
import logging
logging.basicConfig(level=logging.INFO)

from camera import CameraManager
from networktables import NetworkTable

# connect to roborio
NetworkTable.initialize(server='127.0.0.1')

# connect to web cam and start mjpeg server
cam = CameraManager(webcam_device=0, webcam_name="front_camera", local_port=8085, calc="peg")
#cam2 = CameraManager(webcam_device=1, webcam_name="rear_camera", local_port=8086, calc="boiler")

# attempt first read frame
cam.read()
#cam2.read()

while cam.connected:
#while cam.connected and cam2.connected:
  cam.read()
  #cam2.read()
