import time
import threading
import math
import numpy as np

import board
import busio
import adafruit_mcp4728


class NewFinalController():

    def __init__(self):

        self.yValues = np.zeros(shape=(4, 1002))

        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.mcp4728 =  adafruit_mcp4728.MCP4728(self.i2c)

    def streamValues(self):

        startTime = self.startTime
        try:
            while True:
                actualTime = time.time()
                queuePos = (int(actualTime*100) - int(startTime*100)) % 1002
                self.mcp4728.channel_a.value = int(self.yValues[0][queuePos])
                self.mcp4728.channel_b.value = int(self.yValues[1][queuePos])
                self.mcp4728.channel_c.value = int(self.yValues[2][queuePos])
                self.mcp4728.channel_d.value = int(self.yValues[3][queuePos])
                time.sleep(0.001)
        
        except KeyboardInterrupt:
            pass
    
    def setValues(self, newValues):
        yValues = np.zeros(shape=(4, 1002))


        for i in range(4):
            for j in range(1002):
                newValue = int(32767 + newValues[i][j]*32767/200)
                if newValue < 0:
                    yValues[i][j] = 0
                elif newValue > 65535:
                    yValues[i][j] = 65535
                else:    
                    yValues[i][j] = newValue
        
        self.yValues = yValues


    def startStreaming(self, startTime):
        self.startTime = startTime
        t1 = threading.Thread(target=self.streamValues)
        t1.start()

NewFinalController = NewFinalController()