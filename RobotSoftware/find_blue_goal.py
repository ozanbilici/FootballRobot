import numpy as np
import cv2

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
    lb = np.array([90,50,50])
    # defining higher blue range
    hb = np.array([130,255,255])
    # masking other color than blue
    mask = cv2.inRange(hsv,lb,hb)
    # defining kernel for erosion
    kernel = np.ones((5,5),np.uint8)
    # Erode
    #mask = cv2.erode(mask,kernel,iterations = 1)
    # Dilate
    mask = cv2.dilate(mask,kernel,iterations = 1)
    # Opening
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # Closing
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    cv2.imshow('MASK', mask)
# find contours in the threshold image
    _,contours,hierarchy = cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    # finding contour with maximum area and store it as best_cnt
    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt

    # finding centroids of best_cnt and draw a circle there
    M = cv2.moments(best_cnt)
    cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    cv2.circle(vid,(cx,cy),5,255,-1)
    return vid


def display_video(input_org,input_fin):
    # Display Video frames
#    cv2.imshow('ORIGINAL',input_org)
    cv2.imshow('Final',input_fin)


def main():
    cap = capture_video_frame(video_channel)
    while True:
        vid = main_frame(cap)
        vid_fin = contour_goal_detection(vid)
        display_video(vid,vid_fin)
        # Get keyboard escape key to stop the video frame
        key = cv2.waitKey(10) & 0xFF
        if key == 27:
            break

##=====================================================##
if __name__ == '__main__':
    main()

