__author__ = 'ozan'

import serial


class Communication:
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
        print 'kicked ball'
        self.ser.write('5:kr\r\n')

    def startCharging(self):
        print 'start charging'
        self.ser.write('5:cr\r\n')

    def stopCharging(self):
        self.ser.write("5:cs\r\n")

    def startDribler(self):
        self.ser.write("5:dr\r\n")

    def stopDribler(self):
        self.ser.write("5:ds\r\n")

    def ifBallCaptured(self):
        try:
            self.ser.write("5:ib\r\n")

            line = self.ser.readline()

            if 'y' in str(line):
                print "Ball Captured : true"
                return True
            else :
                print "Ball Captured : false"
                return False
        except self.ser.SerialTimeoutException:
            print "Ball Captured : timeout false"
            return False


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

    def forwardwitherror(self,speed,error):
        v1 = str(int(speed+error))
        v2 = str(int(speed-error))

        self.ser.write(self.fr+':sd'+v1+'\r\n')
        self.ser.write(self.fl+':sd-'+v2+'\r\n')
        self.ser.write(self.br+':sd'+v1+'\r\n')
        self.ser.write(self.bl+':sd-'+v2+'\r\n')

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
        self.ser.write(self.fl+':sd0\r\n')
        self.ser.write(self.br+':sd0\r\n')
        self.ser.write(self.bl+':sd0\r\n')

    def connect(self):
        self.ser = serial.Serial('/dev/ttyUSB0',19200, timeout=.1)

        try :
            self.ser.isOpen()
        except serial.serialutil.SerialException:
            print("Cannot open port")

