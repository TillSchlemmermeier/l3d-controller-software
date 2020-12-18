import numpy as np
import os
from multiprocessing import shared_memory
from generators.g_ellipsoid import gen_ellipsoid

class g_sound_circle():
    def __init__(self):
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

        self.size = 1.0
        self.channel = 0

    def return_values(self):
        return [b'sound_ellipsoid', b'amount', b'channel', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.size)), str(self.channel), '', ''),'utf-8')

    def __call__(self, args):
        self.size = args[0]*7+1.0
        self.channel = int(args[1]*3)

        current_volume = self.amount*float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))**4

        # create empty world
        world = np.zeros([3, 10, 10, 10])

        world[0, :, :, :] = gen_ellipsoid(5,self.ysize * volume2+0.01,0.01) - gen_ellipsoid(5*0.8,(self.ysize * volume2+0.01)*0.8,0.01)
        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        return np.clip(world,0,1)
