from MCP4922 import MCP4922
import RPi.GPIO as GPIO
import time
import sys
import math

GPIO.setmode(GPIO.BOARD)

Controller2 = MCP4922(spiBus=0, spiDevice=0, chipSelect=26)
Controller = MCP4922(spiBus=0, spiDevice=1, chipSelect=24)


omega11 =2*math.pi*10
omega12 = 2*math.pi*15

omega21 =2*math.pi*5
omega22 = 2*math.pi*10

try:
    while True:
        for i in range(1000):
            t = i/1000
            l = (math.cos(t*omega11)+1 + math.cos(omega12*t + 1.4)*0.5 +0.5)*1333
            r = (math.cos(t*omega21)+1 + math.cos(omega22*t +1.4)*0.5 +0.5)*1333
            Controller.setValue(l, 0)
            Controller.setValue(l,1)
            Controller2.setValue(r, 0)
            Controller2.setValue(r,1)
            time.sleep(0.001)


except KeyboardInterrupt:
    Controller.setValue(0, 0)
    Controller.setValue(0, 1)
    Controller.shutdown(0)
    Controller.shutdown(1)
    GPIO.cleanup()
    sys.exit()
