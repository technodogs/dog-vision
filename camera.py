import math
import cv2
import cscore as cs
from grip import GripPipeline
from networktables import NetworkTable
import logging
logging.basicConfig(level=logging.INFO)

class CameraManager:
  __camera = None
  __cvsource = None
  __mjpeg_server = None
  __grip_pipeline = None

  __camera_good = False
  __frame = None
  __webcam_name = None
  __calc = None

  # if local development, turn on debug to show frames in a window
  __debug = True

  def __init__(self, webcam_device, webcam_name, local_ip="127.0.0.1", local_port=8087, calc="peg"):
    self.__calc = calc
    
    # start web cam and set dimensions
    self.__camera = cv2.VideoCapture(webcam_device)
    self.__camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    self.__camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # setup cv source to write frames to for mjpeg server
    self.__cvsource = cs.CvSource(webcam_name, cs.VideoMode.PixelFormat.kMJPEG, 320, 240, 30)

    # setup mjpeg server
    self.__mjpeg_server = cs.MjpegServer("httpserver", local_port)
    self.__mjpeg_server.setSource(self.__cvsource);

    # setup grip pipeline from grip.py
    self.__grip_pipeline = GripPipeline()

    # write camera info
    table = NetworkTable.getTable("CameraPublisher")
    cam = table.getSubTable(webcam_name)

    cam.putString("source", "usb:IMAQdx/")
    cam.putStringArray("streams", ["mjpg:http://" + local_ip + ":" + str(local_port) + "/stream.mjpg?name="+webcam_name])

    if self.__debug:
      self.__webcam_name = webcam_name
      cv2.namedWindow(self.__webcam_name)

  def read(self):
    #read from the web camera
    self.__camera_good, frame = self.__camera.read()
    
    if self.__camera_good:
      #run the grip pipeline
      self.__grip_pipeline.process(frame)

      #write the contours onto the frame
      cv2.drawContours(frame, self.__grip_pipeline.filter_contours_output, -1, (0,255,0), 3)

      #write the frame to the mjpeg server
      self.__cvsource.putFrame(frame)

      #run distance calculations
      self.calculate(self.__grip_pipeline.filter_contours_output)
      
      if self.__debug:
        cv2.imshow(self.__webcam_name, frame)
        key = cv2.waitKey(5)
      
  def calculate(self, contours):
    ratios = []
    distances = []
    centerX = []
    for c in contours:
      x, y, w, h = cv2.boundingRect(c)
      centerX.append( round( x + w / 2, 0) )
      ratios.append( round( (float)(w) / h, 2) )

      # distance calc varies by target
      if self.__calc == "peg":
        distances.append(self.calculateGearPeg(h))
      elif self.__calc == "boiler":
        distances.append(self.calculateBoiler(w))
    
    #write calculations to networktables
    self.writeNetworkTables(ratios, distances, centerX)

  def calculateGearPeg(self, h):
    return round( ((5 * 480) / (2 * h * math.tan(60) )), 0)

  def calculateBoiler(self, w):
    return round( ((11.5 * 640) / (2 * w * math.tan(60) )), 0)

  def writeNetworkTables(self, ratios, distances, centerX):
    table = NetworkTable.getTable("DogVision")
    sub = table.getSubTable(self.__calc)
    sub.putNumberArray("ratios", ratios)
    sub.putNumberArray("distances", distances)
    sub.putNumberArray("centerX", centerX)

  def connected(self):
    return self.__camera_good