__author__ = 'ozan'

import numpy as np
import cv2
import time
from Communication import *
from Referee import *
import time
import math
import sys
#sys.path.append('/usr/local/include/opencv2')
#import cv2.cv as cv

class Main(threading.Thread) :
    def __init__(self, threadID, name,  Communication, run_event):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

        # motor run
        self.communication =  Communication

        #video channel
        self.video_channel = 0

        #referee signal
        self.mode = 0

        self.modechanging = 1
        self.run_event = run_event

        self.log = 1
        self.team = 'yel'

        ## Kalman Filter
        '''self.kalman = cv2.KalmanFilter(4, 2, 0)
        self.kalman_state = cv2.CreateMat(4, 1, cv2.CV_32FC1)
        self.kalman_process_noise = cv2.CreateMat(4, 1, cv2.CV_32FC1)
        self.kalman_measurement = cv2.CreateMat(2, 1, cv2.CV_32FC1)'''

        self.firsttime = 1

    def capture_video_frame(self,video_channel):
        # capturing video from video channel
        cap = cv2.VideoCapture(video_channel)
        return cap

    def main_frame(self,cap):
        ret, vid = cap.read()
        vid = cv2.flip(vid,0)
        vid = cv2.flip(vid,1)
        return vid

    def contour_ball_detection(self,vid):
        global mode
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
            mask = cv2.dilate(mask,kernel,iterations = 1)
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
                if self.log == 1:
                    print 'Positions:' + str(cx) + ' ' + str(cy) + ' ' +str(radius) + '\n'
                ctr += 1
                #Printing centroid position in vid
                cv2.putText(vid,pos,(cx+5,cy+5), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0))

            maxcy = max(y)
            find = y.index(maxcy)
            if self.log == 1:
                print 'max cy = ' ,x[find]

            #-----------------------------------------------------------------------

            print 'Positions:' + str(x[find]) + ' ' + str(maxcy)
            #-----------------------------------------------------------------------
            if maxcy == 0 & x[find] == 0:
                self.communication.rotateLeft('30')
            elif  maxcy < 150:
                '''if x[find] < 250:
                    #rotateright
                    print '1'
                    self.communication.rotateLeft('10')
                elif x[find] > 350 :
                    #rotateleft
                    print '2'
                    self.communication.rotateRight('10')
                else:
                    print '3'
                    self.communication.forward('50')'''
                if x[find] < 250:
                    error = 0.014*(350-x[find])
                elif x[find] > 350:
                    error = 0.014*(350-x[find])
                else:
                    error = 0

                self.communication.forwardwitherror(30,error)
                print '1'
            elif 300 > maxcy > 150:
                '''if x[find] < 250:
                    print '4'
                    self.communication.rotateLeft('6')
                elif x[find] > 350:
                    print '5'
                    self.communication.rotateRight('6')
                else:
                    print '6'
                    self.communication.forward('30')'''
                if x[find] < 250:
                    error = 0.014*(350-x[find])
                elif x[find] > 350:
                    error = 0.014*(350-x[find])
                else:
                    error = 0

                self.communication.forwardwitherror(20,error)
                print '2'
            else:
                '''if x[find] <= 200:
                    print '7'
                    self.communication.rotateLeft('4')
                elif x[find] >= 400:
                    print '8'
                    self.communication.rotateRight('4')
                    print '8end'
                else:
                    print '9'
                    self.communication.forward('20')'''
                if x[find] < 250:
                    error = 0.013*(350-x[find])
                elif x[find] > 350:
                    error = 0.013*(350-x[find])
                else:
                    error = 0

                self.communication.forwardwitherror(20,error)
                print '3'

            if self.communication.ifBallCaptured() == True :
                print '10'
                self.mode = 2
                self.modechanging = 1
        except cv2.error, OpenCV_Error :
            print '11'
            print "Can't do the thing"

        except:
            print '12'
            if self.log == 1:
                print "there is no ball"
            self.communication.rotateRight('5')
            return vid

        
        return vid



    def contour_goal_detection(self,vid):
        if self.communication.ifBallCaptured() == False:
            self.modechanging = 1
            self.mode = 1
            return vid
	    #vid = self.main_frame(cv2.VideoCapture(self.video_channel_goal))
        # Applying Gaussian Blur filtering to smooth the image
        gblur_vid = cv2.GaussianBlur(vid,(5,5),0)
        # Changing to HSV colorspace to filter out other color than blue
        hsv = cv2.cvtColor(gblur_vid, cv2.COLOR_RGB2HSV)
        # defining lower blue range
        if self.team == 'blue':
            print 'blue goal'
            # defining lower blue range
            lb = np.array([1,102,32])
            # defining higher blue range
            hb = np.array([10,255,255])
        else:
            print 'yellow goal'
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
            cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
            cv2.circle(vid,(cx,cy),5,255,-1)
            print 'Goal Position:' + str(cx) + ' ' +str (cy)
            # if self.team != 'blue':
            value = math.atan2((600-cy),(300-cx))
            value = value*180/math.pi
            print 'Angle = ' + str(value)
            if cy < 100:
             self.communication.forward('20')
            else:
                if value < 85:
                    print 'rot left'
                    self.communication.rotateLeft('8')
                elif value > 92:
                    print 'rot right'
                    self.communication.rotateRight('8')
                else:
                    self.communication.stop()
                    time.sleep(1)
                if self.log == 1:
                    print 'stop motors'
                self.communication.startCharging()
                if self.log == 1:
                    print 'charge'
                time.sleep(2)
                self.communication.kickBall()
                if self.log == 1:
                    print 'kicked'
                self.mode = 1
                self.modechanging = 1

        except:
            if self.team != 'blue':
                self.communication.rotateLeft('10')
            else:
                self.communication.rotateRight('10')
            if self.log == 1:
                print "no goal founded"
            #self.communication.rotateLeft('30')

        return vid
    def display_video(self,input_org,input_fin):
        # Display Video frames
        if self.log == 1:
            print "display images"
        #cv2.imshow('ORIGINAL',input_org)
        cv2.imshow('Final',input_fin)


    def run(self):
        cap = self.capture_video_frame(self.video_channel)
        while self.run_event.is_set():
            if self.log == 1:
                print self.run_event.is_set()

            if self.mode == 0:
                if self.modechanging == 1:
                    print 'Waiting for referee command'
                    self.communication.stopDribler()
                    self.communication.stop()
          
                    self.modechanging = 0
            elif self.mode == 1:
                if self.modechanging == 1:
                    print 'Tracking ball'
                    self.communication.startDribler()
                    #self.communication.forward('40')
                    self.modechanging = 0
                print 'Mode 1'
                #print "getting frame"
                vid = self.main_frame(cap)
                #print "sending frame"
                vid_fin = self.contour_ball_detection(vid)
                if self.log == 1:
                    self.display_video(vid,vid)
                    key = cv2.waitKey(100) & 0xFF
                    if key==27:
                        break
            elif self.mode == 2:
                if self.modechanging == 1:
                    print 'Kicking ball to the goal'
                    self.modechanging = 0
                vid = self.main_frame(cap)
                vid = self.contour_goal_detection(vid)
                print 'Mode 2 :'
                if self.log == 1:
                    self.display_video(vid,vid)
                    key = cv2.waitKey(100) & 0xFF
                    if key==27:
                        break


if __name__ == '__main__':
    run_event = threading.Event()
    run_event.set()

    communication = Communication()
    communication.connect()

    #------------------------------------------------------
    #Run the referee
    main = Main(0, "Main", communication,run_event)

    #------------------------------------------------------
    #Run the referee
    referee = Referee(1, "Referee", 'B', 'B', main,run_event)
    referee.connect()
    main.start()
    referee.start()

    try:
        while 1:
            pass
    except KeyboardInterrupt:
        print "attempting to close threads"
        run_event.clear()
        print "run event cleared"

        referee.join()
        print "referee thread closed"


        main.join()
        communication.stopDribler()
        communication.stop()
        print "main thread closed"


        print "threads successfully closed"


