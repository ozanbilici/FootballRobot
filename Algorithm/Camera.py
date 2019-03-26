__author__ = 'obilici'

import cv2

class Camera:
    def __init__(self, channel):
        try:
            self.cap = cv2.VideoCapture(channel)
        except:
            print 'Could not open camera'

    def getFrame(self,cap):
        ret, frame = self.cap.read()
        frame = cv2.flip(frame,0)
        frame = cv2.flip(frame,1)
        return frame

    def displayVideo(self, originalFrame, processedFrame):
        cv2.imshow('Original',originalFrame)
        cv2.imshow('Final',processedFrame)