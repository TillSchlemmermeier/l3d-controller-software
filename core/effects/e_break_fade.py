import struct
import numpy as np
from multiprocessing import shared_memory

class e_break_fade():
    '''Effect: Fade during beat breaks, optional S2L brightness during beats'''

    def __init__(self):
        self.fade = 0.0
        self.s2l = 0.0
        self.sound_values = shared_memory.SharedMemory(name="global_s2l_memory")
        self.lastworld = np.zeros([3, 10, 10, 10])
        self.amount = 0.0  # the trail as it eases towards fade or 0

    def return_state(self):
        return [
            ['fade in break', 'fade', round(self.fade, 2)],
            ['s2l in beat', 's2l', round(self.s2l, 2)],
        ]

    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.fade = args[0]
        self.s2l = args[1]
        # === PARAMETERS END ===

        groove = struct.unpack('d', self.sound_values.buf[48:56])[0]
        # the trail eases in and out over about half a second instead of switching
        self.amount += ((0 if groove else self.fade) - self.amount)*0.1
        world = world + self.lastworld*self.amount

        if groove and self.s2l:
            kick = struct.unpack('d', self.sound_values.buf[0:8])[0]
            # quiet dims towards black, a full kick leaves the frame as it is
            world = world*(1 - self.s2l*(1 - min(kick, 1)))

        self.lastworld[:] = world
        return np.clip(world, 0, 1)
