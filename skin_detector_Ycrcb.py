# Takes a set of images as inputs, transforms them using multiple algorithms, then outputs them in CSV format

import sys
import csv
import numpy as np
import cv2
import rgbhycrcb

for imageDimension in [10,20,30,40]:

	outputFile = open(str(imageDimension)+"x"+str(imageDimension)+".csv",'w')

	writer = csv.writer(outputFile,delimiter=',')

	with open("image_paths.txt",'r') as file:
		lines = file.readlines()

	for line in lines:
		imagePath, label = line.split()
	#	if label != 'H':
	#		continue
		print line

		frame = cv2.imread(imagePath) # frame is a HxW numpy ndarray of triplets (pixels), where W and H are the dimensions of the input image
		frame = cv2.resize(frame,(100,100))
		  # downsize it to reduce processing time
		cv2.imshow("original",frame)

		###############################################################################
		# Make everything apart from the main object to be black in color

		skinMask = rgbhycrcb.ThresholdSkin(frame)

		# apply a series of erosions and dilations to the mask using an elliptical kernel
		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
		skinMask = cv2.erode(skinMask, kernel, iterations = 2)
		skinMask = cv2.dilate(skinMask, kernel, iterations = 2)


	#	cv2.imshow("thresholded",bw_image) # Skin color is shown to be completely white
		###############################################################################


		###############################################################################
		# Remove the arm by cropping the image and draw contours around the main object
        h,w = skinMask.shape[:2]
        sign_image = skinMask[:h-15,:]
        _,contours, hierarchy = cv2.findContours(sign_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        largestContourIndex = 0
    	if len(contours)<=0:
    		print "Skipping due to empty contour"
    		continue
    	largestContourArea = cv2.contourArea(contours[largestContourIndex])
    	i=1
    	while i<len(contours):
    		  if cv2.contourArea(contours[i]) > cv2.contourArea(contours[largestContourIndex]):
    			   largestContourIndex = i
    		  i+=1
    	# Draw the largest contour in the image.
    	cv2.drawContours(sign_image,contours,largestContourIndex,(255,255,255),thickness = -1)
    	x,y,w,h = cv2.boundingRect(contours[largestContourIndex]) # Draw a rectangle around the contour perimeter
    	# cv2.rectangle(sign_image,(x,y),(x+w,y+h),(255,255,255),0,8)
    	###############################################################################


    	#######################################################
    	### centre the image in its square ###################
    	squareSide = max(w,h)-1
    	hHalf = (y+y+h)/2
    	wHalf = (x+x+w)/2
    	hMin, hMax = hHalf-squareSide/2, hHalf+squareSide/2
    	wMin, wMax = wHalf-squareSide/2, wHalf+squareSide/2

    	if (hMin>=0 and hMin<hMax and wMin>=0 and wMin<wMax):
    		sign_image = sign_image[hMin:hMax,wMin:wMax]
    	else:
    		print "No contour found!! Skipping this image"
    		continue

    	#cv2.imshow("centred",sign_image)
    	########################################################

    	########################################################
    	# finally convert the multi-dimensonal array of the
    	# image to a one-dimensional one and write it to a file
    	sign_image = cv2.resize(sign_image,(imageDimension,imageDimension))

    	flattened_sign_image = sign_image.flatten() # Convert multi-dimensional array to a one-dimensional array
    	outputLine = [label] + np.array(flattened_sign_image).tolist()
    	writer.writerow(outputLine)
    	cv2.imshow("final",sign_image)
    	#########################################################

    	if cv2.waitKey(1) & 0xFF == ord("q"): # Wait for a few microseconds and check if `q` is pressed.. if yes, then quit
    		break

# cleanup the camera and close any open windows
# camera.release()
cv2.destroyAllWindows()

print "The program completed successfully !!"
