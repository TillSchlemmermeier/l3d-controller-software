# modules
from itertools import cycle
from multiprocessing import shared_memory
import numpy as np
import struct

class g_cube():
    '''
    Generator: cube
    a cube in the cube
    Parameters:
    - size
    - sides y/n : just the edges or also the sides of the cube?
    - s2l channel
    '''

    def __init__(self):
        # parameters
        self.size = 4
        self.sides = False
        self.sizes = cycle([0,1,2,3,4])
        self.growsize = 0
        # s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 'Trigger'
        self.lastvalue = 0
        self.counter = 0
        self.speed = 0
        self.step = 0

    def return_state(self):
        return [
            ['size', 'size', self.size],
            ['surface', 'sides', 'On' if self.sides else 'Off'],
            ['channel', 'channel', self.channel],
            ['speed', 'speed', round(11 - self.speed,2)],
        ]
    
    def __call__(self, args):
        # === PARAMETERS START ===
        self.size = round(args[0]*4)
        self.sides = args[1] > 0.5
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][int(args[2]*5)]
        self.speed = 11 - int(args[3]*10)
        # === PARAMETERS END ===

        # create world
        world = np.zeros([3, 10, 10, 10])
        # create smaller world
        tempworld = np.zeros([10, 10, 10])

        if not self.sides:
            tempworld[:, :, :] = -1.0

        # check if S2L is activated
        if isinstance(self.channel, int):
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]

            # apply threshold
            if current_volume > 0:
                if self.step % self.speed == 0:
                    size = next(self.sizes)
                    self.growsize = size
                else:
                    size = self.growsize
            else:
                size = 0
                self.growsize = 0

        #check for trigger
        elif self.channel == 'Trigger':
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = 0

            if self.counter < 5:
                if self.step % self.speed == 0:
                    size = next(self.sizes)
                    self.counter += 1
                    self.growsize = size
                else:
                    size = self.growsize
            else:
                size = 0
                self.growsize = 0

        else:
            if self.speed < 11:
                if self.step % self.speed == 0:
                    size = next(self.sizes)
                    self.growsize = size
                else:
                    size = self.growsize
            else:
                size = self.size

        # write cube
        # x slices
        tempworld[4-size, 4-size:6+size, 4-size:6+size] += 1
        tempworld[5+size, 4-size:6+size, 4-size:6+size] += 1
        # y slices
        tempworld[4-size:6+size, 4-size, 4-size:6+size] += 1
        tempworld[4-size:6+size, 5+size, 4-size:6+size] += 1
        # z slices
        tempworld[4-size:6+size, 4-size:6+size, 4-size] += 1
        tempworld[4-size:6+size, 4-size:6+size, 5+size] += 1

        # path world together
        for i in range(3):
            world[i, :, :, :] = tempworld

        self.step += 1

        return np.clip(world, 0, 1)
