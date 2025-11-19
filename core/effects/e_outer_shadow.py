# modules
import numpy as np
from effects.gen_outer_shadow_f import outer_shadow
from multiprocessing import shared_memory

class e_outer_shadow():
    def __init__(self):
        self.amount = 1.0
        self.channel = 1
        self.exponent = 1
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.size = 1
        self.amount = 0.0

    def return_state(self):
        return [
            ['exponent', 'exponent', round(self.exponent,2)],
            ['amount', 'amount', round(self.amount,2)],
            ['channel', 'channel', str(self.channel)],
        ]
    
    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.exponent = args[0]*3+1
        self.amount = args[1]
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][round(args[2]*5)]
        # === PARAMETERS END ===

        if isinstance(self.channel, int):
            current_volume = np.clip(float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8')),0,5)
        else:
            current_volume = 1

        bla = outer_shadow(self.exponent*current_volume, 5.5, 5.5, 5.5)*self.amount
        world[0, :, :, :] -= bla
        world[1, :, :, :] -= bla
        world[2, :, :, :] -= bla

        return np.clip(world, 0, 1)
