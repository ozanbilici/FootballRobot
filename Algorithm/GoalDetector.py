__author__ = 'obilici'

import numpy as np
import time
import math
import sys

from Communication import *
from Referee import *
from Camera import *

class GoalDetector:
    def __init__(self):
        self.goalFound = False
        self.cx = 0
        self.cy = 0
        self.angle = 0

    def isFound(self):
        return self.goalFound

    def getPosition(self):
        return self.cx, self.cy, self.angle

    def run(self, team, vid):
        # Applying Gaussian Blur filtering to smooth the image
        gblur_vid = cv2.GaussianBlur(vid,(5,5),0)
        # Changing to HSV colorspace to filter out other color than blue
        hsv = cv2.cvtColor(gblur_vid, cv2.COLOR_RGB2HSV)

        # defining lower blue range
        if team == 'blue':
            # defining lower blue range
            lb = np.array([1,102,32])
            # defining higher blue range
            hb = np.array([10,255,255])
        else:
            # defining lower ysellow range
            lb = np.array([10,144,184])
            # defining higher yellow range
            hb = np.array([109,255,255])

        try:
            # masking other color than blue
            mask = cv2.inRange(hsv,lb,hb)
            #cv2.imshow('Mask',mask)
            # defining kernel for erosion
            kernel = np.ones((5,5),np.uint8)
            # Erode
            #mask = cv2.erode(mask,kernel,iterations = 1)
            # Dilate
            mask = cv2.dilate(mask,kernel,iterations = 1)
            # Opening
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            # Closings
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            # find contours in the threshold image
            _,contours,hierarchy = cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

            # finding contour with maximum area and store it as best_cnt
            max_area = 0

            for cnt in contours:
                ((ax, ay), radius) = cv2.minEnclosingCircle(cnt)
                if self.team != 'blue':
                    if radius > 100:
                        area = cv2.contourArea(cnt)
                        if area > max_area:
                            max_area = area
                            best_cnt = cnt
                else:
                    area = cv2.contourArea(cnt)
                    if area > max_area:
                        max_area = area
                        best_cnt = cnt

            # finding centroids of best_cnt and draw a circle there
            M = cv2.moments(best_cnt)
            self.cx, self.cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])

            cv2.circle(vid, (self.cx, self.cy), 5, 255,-1)

            self.angle = math.atan2((600 - self.cy), (300 - self.cx))
            self.angle = self.angle*180/math.pi

        except:
            self.ballFound = False

        return vid