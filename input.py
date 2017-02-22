''' this file contains the functions for reading the source video of live stream through camera
    and converting the image into desired output with subtracting the backgrund and extracting
    the hand out of the picture frame  '''



import cv2
import numpy as np



def read_through_camera():
  return cv2.VideoCapture(0)

def read_through_video(location):
  return cv2.VideoCapture(location)