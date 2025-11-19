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
        self.channel = 'noS2L'

    def return_state(self):
        return [
            ['exponent', 'exponent', round(self.exponent,1)],
            ['channel', 'channel', self.channel],
        ]

    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.exponent = 0.5 + args[0]*2
        self.channel = ['noS2L', 0, 1, 2, 3][round(args[1]*4)]
        # === PARAMETERS END ===

        # check if s2l is activated
        if isinstance(self.channel, int):
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
