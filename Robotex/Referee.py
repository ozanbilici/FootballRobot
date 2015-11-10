__author__ = 'ozan'

import threading
import serial

class Referee (threading.Thread):
    def __init__(self, threadID, name, robotid, fieldid):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.robotid = robotid
        self.fieldid = fieldid
        self.mode = 0

    def run(self):
        while True:
            counter = 0
            line = []

            for c in self.ser.read():
                line.append(c)
                if c == '-':
                    counter +=1

                    if counter == 4:
                        print("Line: " + line)
                        break

            if line == "a"+self.fieldid+self.robotid+"START----" or line == "a"+self.fieldid+"XSTART----":
                print("START operation is received")
                self.mode = 0
                self.ser.write("a"+self.fieldid+self.robotid+"ACK-----")
            elif line == "a"+self.fieldid+self.robotid+"START----" or line == "a"+self.fieldid+"XSTART----":
                print("STOP operation is received")
                self.mode = 1
                self.ser.write("a"+self.fieldid+self.robotid+"ACK-----")

    def connect(self):
        self.ser = serial.Serial('/dev/ttyACM0',19200)