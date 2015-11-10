__author__ = 'ozan'

import numpy as np
import cv2

from Motor import *
from Referee import *

# 0 for stopping , 1 for moving
status_move = 0

# motor run
motor = Motor()

#referee
referee = Referee(1, "Thread-1", "A", "A")

#referee signal
start = 0

# This value may change due to input point
video_channel = 0


def capture_video_frame(video_channe):
    # capturing video from video channel
    cap = cv2.VideoCapture(video_channel)
    return cap

def main_frame(cap):
    # returning video from video captured
    ret, vid = cap.read()
    return vid

def contour_goal_detection(vid):
    # Applying Gaussian Blur filtering to smooth the image
    gblur_vid = cv2.GaussianBlur(vid,(5,5),0)
    # Changing to HSV colorspace to filter out other color than blue
    hsv = cv2.cvtColor(gblur_vid, cv2.COLOR_BGR2HSV)
    # defining lower blue range
    lo = np.array([5,125,125])
    # defining higher blue range
    ho = np.array([15,255,255])
    # masking other color than blue
    mask = cv2.inRange(hsv,lo,ho)
    # defining kernel for erosion
    kernel = np.ones((3,3),np.uint8)
    # Erode
    mask = cv2.erode(mask,kernel,iterations = 1)
    # Dilate
    mask = cv2.dilate(mask,kernel,iterations = 1)
    # find contours in the threshold image
    _,contours,hierarchy = cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    # Drawing contours
    cv2.drawContours(vid, contours, -1, (0,255,0), 3)


    for i in contours:
    # Moments
        m = cv2.moments(i)
        # Centroid
        try:
            status_move = 1
            cx = int(m['m10']/m['m00'])
            cy = int(m['m01']/m['m00'])
            pos = str(cx) + ' ' + str(cy)

	        #Printing centroid position in vid
            cv2.putText(vid,pos,(cx+5,cy+5), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0))
        except:
            #if status_move == 1:
                #motor.stop();

            move_status = 0
            pass
    return vid


def display_video(input_org,input_fin):
    # Display Video frames
#    cv2.imshow('ORIGINAL',input_org)
    cv2.imshow('Final',input_fin)


def main():
    cap = capture_video_frame(video_channel)
    while True:
        if referee.mode == 1:
            vid = main_frame(cap)
            vid_fin = contour_goal_detection(vid)
            display_video(vid,vid_fin)
            # Get keyboard escape key to stop the video frame
            key = cv2.waitKey(10) & 0xFF
            if key == 27:
                break



if __name__ == '__main__':
    #motor.connect()
    #referee.connect()
    referee.start()
    main()