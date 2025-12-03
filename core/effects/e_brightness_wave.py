# modules
import numpy as np
from multiprocessing import shared_memory
import struct

class e_brightness_wave():

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

    def return_state(self):
        return [
            ['FreqY', 'freq1', round(self.freq1,2)],
            ['FreqZ', 'freq2', round(self.freq2,2)],
            ['step', 'stepincrease', round(self.stepincrease,2)],
            ['channel', 'channel', self.channel],
        ]
    
    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.freq1 = args[0]
        self.freq2 = args[1]
        self.stepincrease = args[2]*0.5
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][round(args[3]*5)]
        # === PARAMETERS END ===


        map = np.sin(self.freq1 * self.mapY + self.step) * np.sin(self.freq2 * self.mapZ + self.step)

        map = np.round(4 * map ,0).astype(int)

        brightness_world = np.zeros([3, 10, 10, 10])

        for y in range(10):
            for z in range(10):
                brightness_world[:,map[y,z]+5,y,z] = 1.0

        world *= brightness_world

        # check if S2L is activated
        if isinstance(self.channel, int):
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
            self.step += current_volume

        #check for trigger
        elif self.channel == 'Trigger':
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
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
