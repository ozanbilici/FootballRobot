__author__ = 'obilici'

import numpy as np
import time
import math
import sys

from Communication import *
from Referee import *
from Camera import *
from Player import *
from GoadDetector import *
from BallDetector import *

if __name__ == '__main__':
    #------------------------------------------------------
    #Referee Signal
    refereeSignal = threading.Event()
    refereeSignal.set()

    #------------------------------------------------------
    #Run the referee
    communication = Communication()
    communication.connect()

    #------------------------------------------------------
    #Run the referee
    player = Player(0, "Player", 'yel', communication, refereeSignal)

    #------------------------------------------------------
    #Run the referee
    referee = Referee(1, "Referee", 'B', 'B', player, refereeSignal)
    referee.connect()

    #------------------------------------------------------
    # Start Game
    player.start()
    referee.start()

    try:
        while 1:
            pass
    except KeyboardInterrupt:
        run_event.clear()
        referee.join()
        player.join()

        communication.stopDribler()
        communication.stop()


