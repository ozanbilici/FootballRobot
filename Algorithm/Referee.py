__author__ = 'obilici'

import threading
import serial

class Referee (threading.Thread):
    def __init__(self, threadID, name, robotid, fieldid, player, refreeSignal):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.robotid = robotid
        self.fieldid = fieldid
        self.player = player
        self.refreeSignal = refreeSignal

    def connect(self):
        self.ser = serial.Serial('/dev/ttyACM0',19200,timeout=.1)

    def sendAck(self):
        try:
            self.ser.write("a"+self.fieldid+self.robotid+"ACK-----")
        except self.ser.SerialTimeoutException:
            print "Timeout : " + command

    def processCommand(self, line):
        if line == "a"+self.fieldid+self.robotid+"START----" or line == "a"+self.fieldid+"XSTART----":
            self.player.changeMode(player.SEARCHING_FOR_BALL)
            self.sendAck()
        elif line == "a"+self.fieldid+self.robotid+"STOP----" or line == "a"+self.fieldid+"XSTOP----":
            self.player.changeMode(player.WAITING_FOR_REFREE)
            self.sendAck()

    def getCommand(self):
        saving = False
        counter = 0
        line = ''

        for c in self.ser.read():
            if c == 'a':
                saving = True

            if saving == True:
                line += c

                if c == '-':
                    counter +=1

                if counter == 4:
                    counter = 0
                    break

    def run(self):
        while self.refreeSignal.is_set():
            try:
                line = self.getCommand()
                self.processCommand(line)
            except self.ser.SerialTimeoutException:
                pass


