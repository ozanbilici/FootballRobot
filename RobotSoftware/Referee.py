__author__ = 'ozan'

import threading
import serial

class Referee (threading.Thread):
    def __init__(self, threadID, name, robotid, fieldid,main,run_event):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.robotid = robotid
        self.fieldid = fieldid
        self.main = main
        self.run_event = run_event

    def run(self):
        counter = 0
        line = ''
        saving = 0

        while self.run_event.is_set():
            try:
                for c in self.ser.read():

                    if c == 'a':
                        saving = 1

                    if saving == 1:
                        line += c

                        if c == '-':
                            counter +=1

                        if counter == 4:
                            counter = 0
                            saving = 0
                            print 'Line' + line
                            break
                print line
                if line == "a"+self.fieldid+self.robotid+"START----" or line == "a"+self.fieldid+"XSTART----":
                    print("START operation is received")
                    self.main.mode = 1
                    self.modechanging = 1
                    self.ser.write("a"+self.fieldid+self.robotid+"ACK-----")
                elif line == "a"+self.fieldid+self.robotid+"STOP----" or line == "a"+self.fieldid+"XSTOP----":
                    print("STOP operation is received")
                    self.main.mode = 0
                    self.modechanging = 1
                    self.ser.write("a"+self.fieldid+self.robotid+"ACK-----")

                if saving == 0:
                    line = ''
            except self.ser.SerialTimeoutException:
                pass

    def connect(self):
        self.ser = serial.Serial('/dev/ttyACM0',19200,timeout=.1)
