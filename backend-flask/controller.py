import numpy as np
import time
import threading
import math
import matplotlib.pyplot as plt

# controller to handle output

class AudioController():

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.channelValues = np.zeros(10020)

        #self.stream = self.p.open(format=pyaudio.paFloat32,
        #                    channels=1,
        #                    rate=1000,
        #                    frames_per_buffer=1,
        #                    output=True
        #                    )
        self.channelValues = self.createTestData()
        self.run()


    def updateValues(self, data):
        print('I am updating ...')
        newValues = np.array([])
        for j in range(501):
            partValues= np.ones(10)
            #partValues = np.ones(20)
            firstValue1 = data[0][j]
            firstValue2 = data[1][j]

            if j != 500:
                nextValue1 = data[0][j+1]
                nextValue2 = data[1][j+1]
                for k in range(10):
                    partValues[k] = firstValue1 + k/10 * (nextValue1 - firstValue1)
                    #partValues[2*k] = firstValue1 + k/10 * (nextValue1 - firstValue1)
                    #partValues[2*k + 1] += firstValue2 + k/10 * (nextValue2 - firstValue2)
                    #partValues[2*k] = firstValue1
                    #partValues[2*k+1] = firstValue2
            else:
                for k in range(10):
                    partValues[k] = firstValue1
                    #partValues[2*k] = firstValue1
                    #partValues[2*k + 1] += firstValue2

            newValues = np.concatenate((newValues, partValues), axis = None)  
        self.channelValues = newValues
        plt.plot(self.channelValues)
        plt.show()
    
    def streamValues(self):
        #while True:
            #print(time.time())
            #valuesToStream = self.channelValues
            #self.stream.write(valuesToStream.astype(np.float32).tostring())
        while True:
            time.sleep(5)
    
    def createTestData(self):
        #values = np.random.randint(10, size=(1000, 1))
        values = np.zeros(shape=(1000, 1))
        #values.astype(float)
        omega1 = 2*math.pi/200
        omega2 = 2*math.pi/3

        for i in range(1000):
            value1 =0.8 + math.sin(i*omega1)*0.3
            #value2 = math.sin(i*omega2)*5
            # if(i % 30 < 15):
            #     value1 = 15
            #     value2 = 15
            # else:
            #     value1 = -15
            #     value2 = -15
            
            newValue = np.array([value1])
            values[i] = newValue

        return values
    
    def run(self):
        print("runned")
        t1 = threading.Thread(target=self.streamValues)
        t1.start()

Controller = AudioController()