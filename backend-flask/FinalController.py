import time
import threading
import math
import numpy as np
import RPi.GPIO as GPIO
from MCP4922 import MCP4922


class FinalController():

    def __init__(self):

        self.yValues = np.zeros(shape=(4, 1002))

        GPIO.setmode(GPIO.BOARD)
        self.DriverL = MCP4922(spiBus=0, spiDevice=0, chipSelect=24)
        self.DriverR = MCP4922(spiBus=0, spiDevice=1, chipSelect=26)

    def streamValues(self):

        startTime = self.startTime
        try:
            while True:
                actualTime = time.time()
                queuePos = (int(actualTime*100) - int(startTime*100)) % 1002

                self.DriverL.setValue(self.yValues[0][queuePos], 0)
                self.DriverL.setValue(self.yValues[1][queuePos], 1)
                self.DriverR.setValue(self.yValues[2][queuePos], 0)
                self.DriverR.setValue(self.yValues[3][queuePos], 1)
                time.sleep(0.001)
        
        except KeyboardInterrupt:
            pass
    
    def setValues(self, newValues):
        yValues = np.zeros(shape=(4, 1002))

        for i in range(4):
            for j in range(1002):
                yValues[i][j] = int(2048 + newValues[i][j]*2048/50)
        
        self.yValues = yValues


    def startStreaming(self, startTime):
        self.startTime = startTime
        t1 = threading.Thread(target=self.streamValues)
        t1.start()

FinalController = FinalController()
