import spidev
import RPi.GPIO as GPIO

# driver for MCP4922


class MCP4922():

    def __init__(self, spiBus=0, spiDevice=1, chipSelect=24):
        
        self.spiBus = spiBus
        self.spiDevice = spiDevice
        self.chipSelect = chipSelect
        
        GPIO.setup(self.chipSelect, GPIO.OUT)
        GPIO.output(self.chipSelect, 1)
        self.device = spidev.SpiDev()
        self.device.open(self.spiBus, self.spiDevice)


    def setValue(self, value, channel=0, double=False):

        bits15_08 = 0b00110000
        bits07_00 = 0b00000000

        valueBits11_08 = (value - (value % 256))/256
        valueBits07_00 = value % 256

        if channel == 1:
            bits15_08 += 128
        
        if double:
            bits15_08 -= 32

        bits15_08 += valueBits11_08
        bits07_00 += valueBits07_00

        GPIO.output(self.chipSelect, 0)
        self.device.writebytes([int(bits15_08), int(bits07_00)])
        GPIO.output(self.chipSelect, 1)
    
    def shutdown(self, channel):

        if channel == 0:
            bits15_08 = 0b00000000

        if channel == 1:
            bits15_08 = 0b10000000

        bits07_00 = 0b00000000 

        GPIO.output(self.chipSelect, 0)
        self.device.writebytes([int(bits15_08), int(bits07_00)])
        GPIO.output(self.chipSelect, 1)






