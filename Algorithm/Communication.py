__author__ = 'obilici'

import serial
import ICommunication

class Communication(ICommunication):
    def __init__(self):
        self.fl = '2'
        self.bl = '3'
        self.br = '4'
        self.fr = '1'

        self.ser = None

    def connect(self):
        self.ser = serial.Serial('/dev/ttyUSB0',19200, timeout=.1)

        try :
            self.ser.isOpen()
        except serial.serialutil.SerialException:
            print("Cannot open port")


    def sendCommand(self, command)
        try:
            self.ser.write(command)
        except self.ser.SerialTimeoutException:
            print "Timeout : " + command

    def kickBall(self):
        self.sendCommand('5:kr\r\n')

    def startCharging(self):
        self.sendCommand('5:cr\r\n')

    def stopCharging(self):
        self.sendCommand("5:cs\r\n")

    def startDribler(self):
        self.sendCommand("5:dr\r\n")

    def stopDribler(self):
        self.sendCommand("5:ds\r\n")

    def moveForward(self,speed):
        self.sendCommand(self.fr+':sd'+speed+'\r\n')
        self.sendCommand(self.fl+':sd-'+speed+'\r\n')
        self.sendCommand(self.br+':sd'+speed+'\r\n')
        self.sendCommand(self.bl+':sd-'+speed+'\r\n')

    def moveForwardWithError(self,speed,error):
        v1 = str(int(speed+error))
        v2 = str(int(speed-error))

        self.sendCommand(self.fr+':sd'+v1+'\r\n')
        self.sendCommand(self.fl+':sd-'+v2+'\r\n')
        self.sendCommand(self.br+':sd'+v1+'\r\n')
        self.sendCommand(self.bl+':sd-'+v2+'\r\n')

    def moveBackward(self,speed):
        self.sendCommand(self.fr+':sd-'+speed+'\r\n')
        self.sendCommand(self.fl+':sd'+speed+'\r\n')
        self.sendCommand(self.br+':sd-'+speed+'\r\n')
        self.sendCommand(self.bl+':sd'+speed+'\r\n')

    def moveRight(self,speed):
        self.sendCommand(self.fr+':sd-'+speed+'\r\n')
        self.sendCommand(self.fl+':sd-'+speed+'\r\n')
        self.sendCommand(self.br+':sd'+speed+'\r\n')
        self.sendCommand(self.bl+':sd'+speed+'\r\n')

    def moveLeft(self,speed):
        self.sendCommand(self.fr+':sd'+speed+'\r\n')
        self.sendCommand(self.fl+':sd'+speed+'\r\n')
        self.sendCommand(self.br+':sd-'+speed+'\r\n')
        self.sendCommand(self.bl+':sd-'+speed+'\r\n')

    def rotateLeft(self,speed):
        self.sendCommand(self.fr+':sd'+speed+'\r\n')
        self.sendCommand(self.fl+':sd'+speed+'\r\n')
        self.sendCommand(self.br+':sd'+speed+'\r\n')
        self.sendCommand(self.bl+':sd'+speed+'\r\n')

    def rotateRight(self,speed):
        self.sendCommand(self.fr+':sd-'+speed+'\r\n')
        self.sendCommand(self.fl+':sd-'+speed+'\r\n')
        self.sendCommand(self.br+':sd-'+speed+'\r\n')
        self.sendCommand(self.bl+':sd-'+speed+'\r\n')

    def stop(self):
        self.sendCommand(self.fr+':sd0\r\n')
        self.sendCommand(self.fl+':sd0\r\n')
        self.sendCommand(self.br+':sd0\r\n')
        self.sendCommand(self.bl+':sd0\r\n')

    def isBallCaptured(self):
        status = False
        try:
            self.sendCommand("5:ib\r\n")
            line = self.ser.readline()
            if 'y' in str(line):
                status = True
        except self.ser.SerialTimeoutException:
            print "Timeout : ifBallCaptured"

        return status
