import cv2
import cscore as cs
from grip import GripPipeline

class CameraManager:
  __camera = None
  __cvsource = None
  __mjpeg_server = None
  __grip_pipeline = None

  __camera_good = False
  __frame = None

  # if local development, turn on debug to show frames in a window
  __debug = False

  def __init__(self, webcam_number, webcam_name):
    # start web cam and set dimensions
    self.__camera = cv2.VideoCapture(webcam_number)
    self.__camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    self.__camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # setup cv source to write frames to for mjpeg server
    self.__cvsource = cs.CvSource(webcam_name, cs.VideoMode.PixelFormat.kMJPEG, 320, 240, 30)

    # setup mjpeg server
    self.__mjpeg_server = cs.MjpegServer("httpserver", 8087)
    self.__mjpeg_server.setSource(self.__cvsource);

    # setup grip pipeline from grip.py
    self.__grip_pipeline = GripPipeline()

    if self.__debug:
      cv2.namedWindow("preview")

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
      
      if self.__debug:
        cv2.imshow("preview", frame)
        key = cv2.waitKey(20)
      
      # i = 1
      # for c in contours:
      #   x, y, w, h = cv2.boundingRect(c)
      #   # distance = ((5 * 480) / (2 * h * math.tan(60) ))
      #   distance = ((11.5 * 640) / (2 * w * math.tan(60) ))
      #   logging.info(str(i) + " " + str(h) + " " + str(distance))
      #   i = i + 1

  def connected(self):
    return self.__camera_good