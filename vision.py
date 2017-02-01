
import numpy
import math
import logging

import cv2
import cscore as cs
from camera import CameraManager

logging.basicConfig(level=logging.INFO)

camera_name = "front camera"

# connect to web cam and start mjpeg server
cam = CameraManager(1, camera_name)

# attempt first read frame
cam.read()

while cam.connected:
  cam.read()
