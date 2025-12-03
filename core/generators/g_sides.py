# modules
import struct
import numpy as np
from random import randint, uniform
from colorsys import hsv_to_rgb
from multiprocessing import shared_memory

class g_sides():
    '''
    Generator: sides
    One side of a cube is on

    Parameters:
    size of cube
    time before choosing new side
    Random color of side On / Off
    Sound2Light channel / Trigger
    '''

    def __init__(self):
        self.size = 4
        self.sides = True
        self.side = 0
        self.randomcolor = False
        self.counter = 1
        self.reset = 1
        # s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0

        self.safeworld = np.zeros([3, 10, 10, 10])

    def return_state(self):
        return [
            ['Size', 'size', round(self.size,2)],
            ['Wait', 'reset', round(self.reset,2)],
            ['Color', 'randomcolor', 'On' if self.randomcolor else 'Off'],
            ['Channel', 'channel', self.channel],
        ]

    def __call__(self, args):
        # === PARAMETERS START ===
        self.size = round(args[0]*4)
        self.reset = int(args[1]*10+1)
        self.randomcolor = args[2] > 0.5
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][int(args[3]*5)]
        # === PARAMETERS END ===


        # create world
        world = np.zeros([3, 10, 10, 10])
        # create smaller world
        tempworld = np.zeros([10, 10, 10])


        if not self.sides:
            tempworld[:, :, :] = -1.0

        size = self.size

        # check if S2L is activated
        if isinstance(self.channel, int):
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
            if current_volume > 0:
                # select side
                self.side = randint(0, 5)

        #check for trigger
        elif self.channel == 'Trigger':
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                # select side
                oldside = self.side

                while True:
                    self.side = randint(0, 5)

                    if self.side != oldside:
                        break

        else:
            # select side
            oldside = self.side

            while True:
                self.side = randint(0, 5)

                if self.side != oldside:
                    break

        if self.counter % self.reset == 0:
            if self.side == 0:
                tempworld[4-size, 4-size:6+size, 4-size:6+size] += 1
            elif self.side == 1:
                tempworld[5+size, 4-size:6+size, 4-size:6+size] += 1
            elif self.side == 2:
                tempworld[4-size:6+size, 4-size, 4-size:6+size] += 1
            elif self.side == 3:
                tempworld[4-size:6+size, 5+size, 4-size:6+size] += 1
            elif self.side == 4:
                tempworld[4-size:6+size, 4-size:6+size, 4-size] += 1
            elif self.side == 5:
                tempworld[4-size:6+size, 4-size:6+size, 5+size] += 1

            for i in range(3):
                world[i, :, :, :] = tempworld

            if self.randomcolor:
                color = hsv_to_rgb(uniform(0, 1), 1, 1)
                for i in range(3):
                    world[i, :, :, :] *= color[i]

        else:
            world = self.safeworld

        self.safeworld = world

        if self.channel != 'Trigger':
            self.counter += 1
        else:
            self.counter = 0

        return np.clip(world, 0, 1)
