import numpy as np
import os
from multiprocessing import shared_memory
from generators.g_ellipsoid import gen_ellipsoid

class g_sound_ellipsoid():
    def __init__(self):
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

        self.xsize = 1.0
        self.ysize = 1.0
        self.zsize = 1.0

    def return_values(self):
        return [b'sound_ellipsoid', b'amount x', b'amount y', b'amount z', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.xsize)), str(round(self.ysize)), str(round(self.zsize)), ''),'utf-8')

    def __call__(self, args):
        self.xsize = args[0]*7+1.0
        self.ysize = args[1]*7+1.0
        self.zsize = args[2]*7+1.0

        volume1 = float(str(self.sound_values.buf[0:8],'utf-8'))
        volume2 = float(str(self.sound_values.buf[8:16],'utf-8'))
        volume3 = float(str(self.sound_values.buf[16:24],'utf-8'))

        # create empty world
        world = np.zeros([3, 10, 10, 10])

        world[0, :, :, :] = gen_ellipsoid(self.xsize * volume1+0.01,self.ysize * volume2+0.01,self.zsize * volume3+0.01)
        world[0, :, :, :] -= gen_ellipsoid(0.5*self.xsize * volume1+0.01,0.5*self.ysize * volume2+0.01,0.5*self.zsize * volume3+0.01)

        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        return np.clip(world,0,1)
