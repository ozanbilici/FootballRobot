import cv2
import numpy as np


cap = cv2.VideoCapture(0)

def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('result')

# Starting with 100's to prevent error while masking
h,s,v = 100,100,100

# Creating track bar
cv2.createTrackbar('h', 'result',0,109,nothing)
cv2.createTrackbar('s', 'result',0,255,nothing)
cv2.createTrackbar('v', 'result',0,255,nothing)

while(1):

    _, frame = cap.read()
    frame = cv2.GaussianBlur(frame,(5,5),0)
    #converting to HSV BGR-RGB
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    h = cv2.getTrackbarPos('h','result')
    s = cv2.getTrackbarPos('s','result')
    v = cv2.getTrackbarPos('v','result')

    # Normal masking algorithm
    lower_blue = np.array([h,s,v])
    upper_blue = np.array([20,255,255])

    mask = cv2.inRange(hsv,lower_blue, upper_blue)
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

    result = cv2.bitwise_and(frame,frame,mask = mask)

    cv2.imshow('result',mask)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()
