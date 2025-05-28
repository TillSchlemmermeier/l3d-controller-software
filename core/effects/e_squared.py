# modules
import numpy as np
from multiprocessing import shared_memory

class e_squared():
    '''
    Effect: sharpen

    Parameters:
    exponent
    Sound2Light channel, volume changes exponent
    '''

    def __init__(self):
        self.exponent = 1.0
        self.old_exponent = 1.0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 4

    def return_state(self):
        if self.channel >= 0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return [
            ['exponent', 'exponent', round(self.exponent,1)],
            ['channel', 'channel', channel],
        ]

    def __call__(self, world, args):
        # parsing input
        self.exponent = 0.5 + args[0]*2
        self.channel = int(args[1]*4)-1

        # check if s2l is activated
        if self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            current_volume = np.clip(current_volume, 0, 1.24)
            new_exponent = 2.5 - current_volume * 2

#            if self.old_exponent < self.exponent:
            self.old_exponent += 0.25
            self.old_exponent = np.clip(self.old_exponent, 0.2, 2.5)

            if self.old_exponent > new_exponent:
                self.old_exponent = new_exponent

            world = world**self.old_exponent

        else:
            world = world**self.exponent

        return np.clip(world, 0, 1)
