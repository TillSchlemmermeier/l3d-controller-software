# modules
import numpy as np
from multiprocessing import shared_memory

class g_sinus():
    '''
    Generator: sinus
    '''
    def __init__(self):
        self.freq1 = 1
        self.freq2 = 1
        self.step = 1
        self.stepincrease = 0.1

        self.mapY = np.zeros([10,10])
        self.mapZ = np.zeros([10,10])
        for i in range(10):
            self.mapY[i,:] = i
            self.mapZ[:,i] = i

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0
        self.counter = 0


    def return_values(self):
        return [b'g_sinus', b'FreqY', b'FreqZ', b'step', b'channel']

    def return_gui_values(self):
        if 4 > self.channel >= 0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = "Trigger"
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.freq1,2)), str(round(self.freq2,2)), str(round(self.stepincrease,2)), channel),'utf-8')


    def __call__(self, args):
        self.freq1 = args[0]
        self.freq2 = args[1]
        self.stepincrease = args[2]*0.5
        self.channel = int(args[3]*5)-1

        world = np.zeros([3, 10, 10, 10])

        map = np.sin(self.freq1 * self.mapY + self.step) * np.sin(self.freq2 * self.mapZ + self.step)

        map = np.round(4 * map ,0).astype(int)

        for y in range(10):
            for z in range(10):
                world[:,map[y,z]+5,y,z] = 1.0

        # check if S2L is activated
        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            self.step += current_volume

        #check for trigger
        elif self.channel == 4:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = 0

            if self.counter < 10:
                self.freq1 += self.counter / 10
                self.freq1 += self.counter / 10
                self.counter += 1

            self.step += self.stepincrease

        else:
            self.step += self.stepincrease

        return world
