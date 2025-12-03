# modules
import struct
import numpy as np
from multiprocessing import shared_memory

class e_randomizer():

    def __init__(self):
        self.amount = 0.5
        self.channel = 4
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

    def return_state(self):
        return [
            ['amount', 'amount', round(self.amount,1)],
            ['channel', 'channel', self.channel],
        ]
    
    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.amount = args[0]
        self.channel = ['noS2L', 0, 1, 2, 3][round(args[1]*4)]
        # === PARAMETERS END ===

        if self.channel == 'noS2L':
            r = np.random.normal(0, self.amount, [10,10,10])
        else:
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
            r = np.random.normal(0, np.clip(current_volume,0,10)*self.amount*2, [10,10,10])

        world[0, :, :, :] = world[0, :, :, :]+r*world[0, :, :, :]
        world[1, :, :, :] = world[1, :, :, :]+r*world[1, :, :, :]
        world[2, :, :, :] = world[2, :, :, :]+r*world[2, :, :, :]

        return np.clip(world, 0, 1)
