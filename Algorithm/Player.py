__author__ = 'obilici'

import numpy as np
import cv2
import time
from Communication import *
from Referee import *
import time
import math
import sys

class Player(threading.Thread) :
    def __init__(self, threadID, name, team, communication, ballDetector, goalDetector, refereeSignal):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

        # Set
        self.communication = communication
        self.ballDetector = ballDetector
        self.goalDetector = goalDetector
        self.refereeSignal = refereeSignal
        self.team = team

        self.camera = Camera(0)

        #video channel
        self.isModeChanged = True
        self.log = 1
        self.firsttime = 1

        #referee signal
        self.WAITING_FOR_REFREE = 0
        self.SEARCHING_FOR_BALL = 1
        self.SEARCHING_FOR_GOAL = 2

        self.mode = WAITING_FOR_REFREE

    def changeMode(self, mode):
        self.mode = mode
        self.isModeChanged = True

    def runBallDetection(self,vid):
        vid = self.ballDetector.run(vid)

        if(self.ballDetector.isFound())
            cx, cy = self.ballDetector.getPosition()

            if cy == 0 & cx == 0:
                self.communication.rotateLeft('30')
            elif  cy < 150:
                if cx < 250:
                    error = 0.014*(350 - cx)
                elif cx > 350:
                    error = 0.014*(350 - cx)
                else:
                    error = 0

                self.communication.forwardwitherror(30,error)

            elif 300 > cy > 150:
                if cx < 250:
                    error = 0.014*(350-cx)
                elif cx > 350:
                    error = 0.014*(350-cx)
                else:
                    error = 0

                self.communication.forwardwitherror(20,error)

            else:
                if cx < 250:
                    error = 0.013*(350-cx)
                elif cx > 350:
                    error = 0.013*(350-cx)
                else:
                    error = 0

                self.communication.forwardwitherror(20,error)

            if self.communication.isBallCaptured() == True :
                self.changeMode(SEARCHING_FOR_GOAL)

        else:
            self.communication.rotateRight('5')

        return vid


    def runGoalDetection(self, id):
        if self.communication.isBallCaptured() == False:
            self.changeMode(SEARCHING_FOR_BALL)
            return vid

        vid = self.goalDetector.run(self.team, vid)

        if(self.goalDetector.isFound())
            cx, cy, angle = self.goalDetector.getPosition()

            if cy < 100:
                self.communication.forward('20')
            else:
                if angle < 85:
                    self.communication.rotateLeft('8')
                elif angle > 92:
                    self.communication.rotateRight('8')
                else:
                    self.communication.stop()
                    time.sleep(1)

                self.communication.startCharging()
                time.sleep(2)
                self.communication.kickBall()

                self.changeMode(SEARCHING_FOR_BALL)

        else:
            if self.team != 'blue':
                self.communication.rotateLeft('10')
            else:
                self.communication.rotateRight('10')

        return vid

    def runStateMachine(self, img):
        if self.mode == WAITING_FOR_REFREE:
            if self.modechanging:
                self.communication.stopDribler()
                self.communication.stop()
                self.modechanging = False

        elif self.mode == SEARCHING_FOR_BALL:
            if self.isModeChanged:
                self.communication.startDribler()
                self.isModeChanged = False

            img = self.runBallDetection(img)

        elif self.mode == SEARCHING_FOR_GOAL:
            self.isModeChanged = False
            img = self.runGoalDetection(img)

    def runLog(self, img):
        if self.log == 1:
            print self.refereeSignal.is_set()
            print self.mode

            self.camera.displayVideo(img,img)
            key = cv2.waitKey(100) & 0xFF
            if key==27:
                break

    def run(self):
        while self.refereeSignal.is_set():
            img = self.camera.getFrame()
            self.runStateMachine(img)
            self.runLog(img)

