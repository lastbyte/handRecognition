import cv2
import numpy as np
from constants import *

def set_frame_dimensions(cap,height,width):
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, width);
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height);
  return cap

def capture_hand_histogram(frame,box_x,box_y):
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  ROI = np.zeros([constants.capture_box_dim * constants.capture_box_count, constants.capture_box_dim, 3], dtype=hsv.dtype)
  for i in range(constants.capture_box_count):
    ROI[i * constants.capture_box_dim:i * constants.capture_box_dim + constants.capture_box_dim, 0:constants.capture_box_dim] = hsv[box_y[i]:box_y[
                                                                                                       i] + constants.capture_box_dim,
                                                                                        box_x[i]:box_x[
                                                                                                   i] + constants.capture_box_dim]

  hand_histogram = cv2.calcHist([ROI], [0, 1], None, [180, 256], [0, 180, 0, 256])
  cv2.normalize(hand_histogram, hand_histogram, 0, 255, cv2.NORM_MINMAX)
  return hand_histogram


def hand_threshold(frame,hand_hist):
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  back_projection = cv2.calcBackProject([hsv], [0, 1], hand_hist, [00, 180, 0, 256], 1)
  disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (constants.morph_elem_size, constants.morph_elem_size))
  #cv2.filter2D(back_projection, -1, disc, back_projection)
  back_projection = cv2.GaussianBlur(back_projection, (constants.gaussian_ksize, constants.gaussian_ksize), constants.gaussian_sigma)
  ret, thresh = cv2.threshold(back_projection, 0, 255, 0)
  kernel = np.ones((5,5),np.uint8)
  thresh = cv2.erode(thresh, kernel, iterations=1)
  thresh = cv2.dilate(thresh, kernel, iterations=1)
  cv2.imshow("", thresh)
  return thresh