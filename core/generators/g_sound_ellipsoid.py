import numpy as np
import struct
from multiprocessing import shared_memory
from generators.g_ellipsoid import gen_ellipsoid

class g_sound_ellipsoid():
    def __init__(self):
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

        self.xsize = 1.0
        self.ysize = 1.0
        self.zsize = 1.0

    def return_state(self):
        return [
            ['amount x', 'xsize', round(self.xsize)],
            ['amount y', 'ysize', round(self.ysize)],
            ['amount z', 'zsize', round(self.zsize)],
        ]

    def __call__(self, args):
        # === PARAMETERS START ===
        self.xsize = args[0]*7+1.0
        self.ysize = args[1]*7+1.0
        self.zsize = args[2]*7+1.0
        # === PARAMETERS END ===

        volume1 = struct.unpack('d', bytes(self.sound_values.buf[0:8]))[0]
        volume2 = struct.unpack('d', bytes(self.sound_values.buf[8:16]))[0]
        volume3 = struct.unpack('d', bytes(self.sound_values.buf[16:24]))[0]

        # create empty world
        world = np.zeros([3, 10, 10, 10])

        world[0, :, :, :] = gen_ellipsoid(self.xsize * volume1+0.01,self.ysize * volume2+0.01,self.zsize * volume3+0.01)
        world[0, :, :, :] -= gen_ellipsoid(0.5*self.xsize * volume1+0.01,0.5*self.ysize * volume2+0.01,0.5*self.zsize * volume3+0.01)

        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        return np.clip(world,0,1)
