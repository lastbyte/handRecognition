import cv2
import numpy as np
from rgbhycrcb import *

frame = cv2.imread('sample/A.jpg')

frame = cv2.resize(frame,(200,200))


skin = ThresholdSkin(frame)
dailation_size = 5
erosion_size = 5

# kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
#
# skinmask = cv2.erode(skin,kernel,iterations=2)
# skinmask = cv2.dilate(skinmask,kernel,iterations=2)

cv2.imshow("skin", skin)
cv2.waitKey()
