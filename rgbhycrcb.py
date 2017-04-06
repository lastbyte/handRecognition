'''
author = Nishant Kumar

an implementation of the rgb_h_ycrcb algorithm for skin detection
'''
import cv2
import numpy as np

def R1(R,G,B):
    R = int(R)
    G = int(G)
    B = int(B)
    e1 = (R>95) and (G>40) and (B>20) and ((max(R,max(G,B)) - min(R, min(G,B)))>15) and (abs(R-G)>15) and (R>G) and (R>B);
    e2 = (R>220) and (G>210) and (B>170) and (abs(R-G)<=15) and (R>B) and (G>B);
    return (e1 or e2);

def R2(Y,Cr,Cb):
    e3 = Cr <= 1.5862*Cb+20;
    e4 = Cr >= 0.3448*Cb+76.2069;
    e5 = Cr >= -4.5652*Cb+234.5652;
    e6 = Cr <= -1.15*Cb+301.75;
    e7 = Cr <= -2.2857*Cb+432.85;
    return (e3 and e4 and e5 and e6 and e7);

def R3(H,S,V):
    return ((H<25) or (H>230))

def ThresholdSkin(frame):


    rows,cols,channel = frame.shape
    dst = np.zeros((rows,cols,1),np.uint8)

    src_ycrcb = cv2.cvtColor(frame,cv2.COLOR_BGR2YCR_CB)
    # OpenCV scales the Hue Channel to [0,180] for
    # 8bit images, make sure we are operating on
    # the full spectrum from [0,360] by using floating
    # point precision:
    src_hsv = frame.astype(np.float32)
    src_hsv = cv2.cvtColor(src_hsv,cv2.COLOR_BGR2HSV)

    # And then scale between [0,255] for the rules in the paper
    # to apply. This uses normalize with CV_32FC3, which may fail
    # on older OpenCV versions. If so, you probably want to split
    # the channels first and call normalize independently on each
    # channel:
    src_hsv = cv2.normalize(src_hsv,0,255,norm_type=cv2.NORM_MINMAX,dtype=cv2.CV_32FC3)
    # iterate over the data
    for i in range(0,rows):
        for j in range(0,cols):
            pixel = frame[i,j]
            B = pixel[0]
            G = pixel[1]
            R = pixel[2]
            # apply the rgb rule
            a = R1(R,G,B)

            pixel = src_ycrcb[i,j]
            Y = pixel[0]
            Cr = pixel[1]
            Cb = pixel[2]
            # apply the YCrCb rule
            b = R2(Y,Cr,Cb)

            pixel = src_hsv[i,j]
            H = pixel[0]
            S = pixel[1]
            V = pixel[2]
            # apply the HSV rule
            c = R3(H,S,V)
            #if not skin then black
            if (a and b and c) :
                dst[i,j] = 255

    return dst
