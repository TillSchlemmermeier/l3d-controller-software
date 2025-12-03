import struct
import numpy as np
from multiprocessing import shared_memory
from random import randint

class e_slicer():

    def __init__(self):
        # parameters
        self.slices = []
        self.number = 5
        self.frames = 5
        for i in range(self.number):
            self.slices.append(randint(0, 9))

        self.channel = 1.0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

        self.counter = 1

    def return_state(self):
        return [
            ['number', 'number', round(self.number,0)],
            ['channel', 'channel', self.channel],
            ['n frames', 'frames', self.frames],
        ]
    
    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.number = int(args[0]*3)+3
        self.channel = int(round(args[1]*3))
        self.frames = int(args[2]*10+5)
        # === PARAMETERS END ===

        current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
        current_volume = np.clip(current_volume, 0, 1)

        brightness = [0 for x in range(10)]

        for i in range(len(self.slices)):
            brightness[self.slices[i]] = current_volume
            current_volume -= 0.1
            current_volume = np.clip(current_volume, 0, 4)

        for i in range(len(brightness)):
            world[:, i, :, :] *= brightness[i]

        self.counter += 1

        if self.counter > self.frames:
            self.counter = 0
            self.slices = []
            for i in range(self.number):
                self.slices.append(randint(0, 9))


        return np.clip(world, 0, 1)
