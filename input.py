''' this file contains the functions for reading the source video of live stream through camera
    and converting the image into desired output with subtracting the backgrund and extracting
    the hand out of the picture frame  '''



import cv2
import numpy as np
from constants import *


def read_through_camera():
  return cv2.VideoCapture(0)

def read_through_video(location):
  return cv2.VideoCapture(location)


# this window will be used for reading the color of the palm
# first and then use the inout for detecting hand in further
#  frames
def create_hand_detection_window (frame,handCaptured):
  capture_box_count = 9
  capture_box_dim = 20
  capture_box_sep_x = 8
  capture_box_sep_y = 18
  if not(constants.handCaptured) :

    cv2.putText(frame, "Place hand inside boxes and press 'h' to capture hand histogram",
                (int(0.08 * frame.shape[1]), int(0.97 * frame.shape[0])), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 255, 255), 1, 8)

    capture_pos_x = int((frame.shape[1]-3*capture_box_dim+2*capture_box_sep_x)/2)
    capture_pos_y = int((frame.shape[0] - 3 * capture_box_dim + 2 * capture_box_sep_y) / 2)

    constants.box_pos_x = np.array([capture_pos_x, capture_pos_x + capture_box_dim + capture_box_sep_x,
                          capture_pos_x + 2 * capture_box_dim + 2 * capture_box_sep_x, capture_pos_x,
                          capture_pos_x + capture_box_dim + capture_box_sep_x,
                          capture_pos_x + 2 * capture_box_dim + 2 * capture_box_sep_x, capture_pos_x,
                          capture_pos_x + capture_box_dim + capture_box_sep_x,
                          capture_pos_x + 2 * capture_box_dim + 2 * capture_box_sep_x], dtype=int)
    constants.box_pos_y = np.array(
      [capture_pos_y, capture_pos_y, capture_pos_y, capture_pos_y + capture_box_dim + capture_box_sep_y,
       capture_pos_y + capture_box_dim + capture_box_sep_y, capture_pos_y + capture_box_dim + capture_box_sep_y,
       capture_pos_y + 2 * capture_box_dim + 2 * capture_box_sep_y,
       capture_pos_y + 2 * capture_box_dim + 2 * capture_box_sep_y,
       capture_pos_y + 2 * capture_box_dim + 2 * capture_box_sep_y], dtype=int)
    for i in range(capture_box_count):
      cv2.rectangle(frame, (constants.box_pos_x[i], constants.box_pos_y[i]),
                    (constants.box_pos_x[i] + capture_box_dim, constants.box_pos_y[i] + capture_box_dim), (255, 0, 0), 1)
  return frame;