import board
import busio
import adafruit_mcp4728

import time
import sys
import math
from datetime import datetime

i2c = busio.I2C(board.SCL, board.SDA)
mcp4728 =  adafruit_mcp4728.MCP4728(i2c)

mcp4728.channel_a.value = int(65535/6) # Voltage = VDD
mcp4728.channel_b.value = int(65535/2) # VDD/2
mcp4728.channel_c.value = int(65535/4) # VDD/4
mcp4728.channel_d.value = 0 # 0V

counter = 0

prevTime = time.time()
try:
    while True:
        now = time.time()
        print(now - prevTime)
        counter += 1
        value = int(10000/2*(1 - math.sin(counter)))
        mcp4728.channel_a.value = value # Voltage = VDD
        mcp4728.channel_b.value = value # Voltage = VDD
        mcp4728.channel_c.value = value # Voltage = VDD
        mcp4728.channel_d.value = value # Voltage = VDD
        prevTime = time.time()

except KeyboardInterrupt:
    pass




mcp4728.save_settings()