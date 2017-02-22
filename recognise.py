from input import *

select = int(input("enter 1 for camera and 2 for sample video ??"))

if select == 1:
  cap = read_through_camera()
else:
  # for testing purpose hard code the location variable
  # location = 'location/of/the/file'
  location = str(input("enter the location of the sample video file"))
  cap = read_through_video();

while cap.isOpened() :
  ret, image = cap.read()