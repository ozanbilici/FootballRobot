__author__ = 'obilici'

import numpy as np
import time
import math
import sys

from Communication import *
from Referee import *
from Camera import *

class BallDetector:
    def __init__(self):
        self.ballFound = False
        self.cx = 0
        self.cy = 0
        self.angle = 0

    def isFound(self):
        return self.ballFound

    def getPosition(self):
        return self.cx, self.cy

    def run(self, vid):
        try:
            # Applying Gaussian Blur filtering to smooth the image
            gblur_vid = cv2.GaussianBlur(vid,(5,5),0)
            # Changing to HSV colorspace to filter out other color than blue
            hsv = cv2.cvtColor(gblur_vid, cv2.COLOR_BGR2HSV)

            # defining lower blue range
            lo = np.array([0,211,178])
            # defining higher blue range
            ho = np.array([20,255,255])

            # masking other color than blue
            mask = cv2.inRange(hsv,lo,ho)
            # defining kernel for erosion
            kernel = np.ones((5,5),np.uint8)
            # Erode
            #mask = cv2.erode(mask,kernel,iterations = 1)
            # Dilate
            mask = cv2.dilate(mask,kernel, iterations = 1)
            # Opening
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            # Closing
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            #cv2.imshow('Mask', mask)
            # find contours in the threshold image
            _,contours,hierarchy = cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            # Drawing contours
            cv2.drawContours(vid, contours, -1, (0,255,0), 3)
            ctr = 0
            x = [0,0,0,0,0,0,0,0,0,0,0]
            y = [0,0,0,0,0,0,0,0,0,0,0]

            for i in contours:
                #print "radius"
                ((ax, ay), radius) = cv2.minEnclosingCircle(i)

                if radius > 100:
                    continue

                #print radius
                # Moments
                m = cv2.moments(i)
                # Centroid

                cx = int(m['m10']/m['m00'])
                cy = int(m['m01']/m['m00'])
                x[ctr] = cx
                y[ctr] = cy
                pos = str(cx) + ' ' + str(cy) + ' ' + str(radius)
                ctr += 1
                #Printing centroid position in vid
                cv2.putText(vid,pos,(cx+5,cy+5), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0))

            maxcy = max(y)
            find = y.index(maxcy)
            if self.log == 1:

            #-----------------------------------------------------------------------
            self.cx = x[find]
            self.cy = maxcy

            self.ballFound = True

        except:
            self.ballFound = False


        return vid