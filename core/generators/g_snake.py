import struct
import numpy as np
from random import randint, uniform, choice
from multiprocessing import shared_memory

class g_snake():
    '''
    Generator: snake

    A snake!

    Parameters:
    - number   : Number of snakes running around
    - turnprop : propability of doing a turn
    '''

    def __init__(self):
        self.number = 1
        self.turnprop = 0.25

        # create an internal world with i snake point
        self.axis = 0
        self.direction = 1

        self.world = np.zeros([3, 10, 10, 10])
        self.world[:, 4, 4, 4] = 1.0
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0

    def return_state(self):
        return [
            ['turn', 'turnprop', round(self.turnprop,2)],
            ['channel', 'channel', self.channel],
        ]
    
    def __call__(self, args):
        # === PARAMETERS START ===
        self.turnprop = 1-args[0]
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][int(args[1]*5)]
        # === PARAMETERS END ===

        world = np.zeros([3,10,10,10])

        # check if S2L is activated
        if isinstance(self.channel, int):
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
            self.turnprop = 1
            if current_volume > 0:
                #choose direction
                oldaxis = self.axis
                while oldaxis == self.axis:
                    self.axis = randint(1, 3)

                self.direction = choice([-1, 1])

        #check for trigger
        elif self.channel == 'Trigger':
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.turnprop = 0
            else:
                self.turnprop = 1

        # choose direction
        if uniform(0, 1) > self.turnprop:

            oldaxis = self.axis
            while oldaxis == self.axis:
                self.axis = randint(1, 3)

            self.direction = choice([-1, 1])

        world = np.roll(self.world, self.direction, self.axis)
        self.world = world

        return np.clip(world, 0, 1)
