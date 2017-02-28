import cv2
from input import *
from imageProcessing import *
from constants import *
#select = int(input("enter 1 for camera and 2 for sample video ??"))
select = 1
if select == 1:
  cap = read_through_camera()
else:
  # for testing purpose hard code the location variable
  # location = 'location/of/the/file'
  location = str(input("enter the location of the sample video file"))
  cap = read_through_video();


#limiting the frame size of the video file
cap = set_frame_dimensions(cap,1200,1200);


# actual part of the code where the detection starts
while cap.isOpened() :

  #extracting frame from the video file
  ret, frame = cap.read()

  # capturing hand histogram
  if not(constants.handCaptured):
    # create rectangles for capturing histogram of the hand
    frame = create_hand_detection_window(frame, constants.handCaptured)

    if cv2.waitKey(1) & 0xFF == ord('h'):
      constants.histogram = capture_hand_histogram(frame,constants.box_pos_x,constants.box_pos_y)
      print(constants.histogram)
      constants.handCaptured = True
  if constants.handCaptured:
    frame = cv2.bilateralFilter(frame,5,200,400)
    frame = cv2.flip(frame, 1)
    frame_th = hand_threshold(frame,constants.histogram)
  else:
    '''need not do anything'''
  cv2.imshow("image with hand frame", frame)
  # exiting the application by pressing q on the keyboard
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
cap.release()
cv2.destroyAllWindows()