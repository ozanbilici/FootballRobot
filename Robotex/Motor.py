__author__ = 'ozan'

import serial


class Motor:
    def __init__(self):
        self.fl = '2'
        self.bl = '3'
        self.br = '4'
        self.fr = '1'

        self.ser = '';


	#
	# 5:ki : kick the ball
	# 5:sc : start charging
	# 5:ib : if ball captured
	# 5:dr : dribler run
	# 5:ds : dribler stop
	#

    def kickBall(self):
        self.ser.write("5:ki\r\n")

    def startCharging(self):
        self.ser.write("5:sc\r\n")

    def startDribler(self):
        self.ser.write("5:dr\r\n")

    def stopDribler(self):
        self.ser.write("5:ds\r\n")

    def ifBallCaptured(self):
        self.ser.write("5:ib\r\n")

        line = []
        counter = 0
        for c in self.ser.read():
            line.append(c)
            if c == '/0':
                print("Ball Captured : " + line)


        return True


    def ifBallCaptured(self):
        self.ser.write("5:ib\r\n")

        line = []
        counter = 0
        for c in self.ser.read():
            line.append(c)
            if c == '/0':
                print("Ball Captured : " + line)


        return True

    def forward(self,speed):
        self.ser.write(self.fr+':sd'+speed+'\r\n')
        self.ser.write(self.fl+':sd-'+speed+'\r\n')
        self.ser.write(self.br+':sd'+speed+'\r\n')
        self.ser.write(self.bl+':sd-'+speed+'\r\n')

    def forward(self,speed):
        self.ser.write(self.fr+':sd'+speed+'\r\n')
        self.ser.write(self.fl+':sd-'+speed+'\r\n')
        self.ser.write(self.br+':sd'+speed+'\r\n')
        self.ser.write(self.bl+':sd-'+speed+'\r\n')

    def backward(self,speed):
        self.ser.write(self.fr+':sd-'+speed+'\r\n')
        self.ser.write(self.fl+':sd'+speed+'\r\n')
        self.ser.write(self.br+':sd-'+speed+'\r\n')
        self.ser.write(self.bl+':sd'+speed+'\r\n')

    def right(self,speed):
        self.ser.write(self.fr+':sd-'+speed+'\r\n')
        self.ser.write(self.fl+':sd-'+speed+'\r\n')
        self.ser.write(self.br+':sd'+speed+'\r\n')
        self.ser.write(self.bl+':sd'+speed+'\r\n')

    def left(self,speed):
        self.ser.write(self.fr+':sd'+speed+'\r\n')
        self.ser.write(self.fl+':sd'+speed+'\r\n')
        self.ser.write(self.br+':sd-'+speed+'\r\n')
        self.ser.write(self.bl+':sd-'+speed+'\r\n')

    def rotateLeft(self,speed):
        self.ser.write(self.fr+':sd'+speed+'\r\n')
        self.ser.write(self.fl+':sd'+speed+'\r\n')
        self.ser.write(self.br+':sd'+speed+'\r\n')
        self.ser.write(self.bl+':sd'+speed+'\r\n')

    def rotateRight(self,speed):
        self.ser.write(self.fr+':sd-'+speed+'\r\n')
        self.ser.write(self.fl+':sd-'+speed+'\r\n')
        self.ser.write(self.br+':sd-'+speed+'\r\n')
        self.ser.write(self.bl+':sd-'+speed+'\r\n')


    def stop(self):
        self.ser.write(self.fr+':sd0\r\n')
        self.ser.write(fl+':sd0\r\n')
        self.ser.write(self.br+':sd0\r\n')
        self.ser.write(self.bl+':sd0\r\n')

    def connect(self):
        self.ser = serial.Serial('/dev/ttyUSB0',19200)

        try :
            self.ser.isOpen()
        except serial.serialutil.SerialException:
            print("Cannot open port")

