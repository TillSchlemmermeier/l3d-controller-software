# modules
from multiprocessing import shared_memory
import numpy as np

class g_soundedges():

    def __init__(self):
        # parameters
        self.size = 4
        # s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

    def return_values(self):
        return [b'soundedges', b'size', b'', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.size, 2)), '', '', ''),'utf-8')

    def __call__(self, args):
        self.size = round(args[0]*5)

        # create world
        world = np.zeros([3, 10, 10, 10])

        length = [0,0,0,0]
        for i in range(4):
            length[i] = float(str(self.sound_values.buf[i*8:i*8+8],'utf-8'))

        world[:, :int(round(np.clip(length[0]*self.size,0, 10))), 0, 0] = 1.0
        world[:, :int(round(np.clip(length[1]*self.size,0, 10))), 0, 9] = 1.0
        world[:, :int(round(np.clip(length[2]*self.size,0, 10))), 9, 0] = 1.0
        world[:, :int(round(np.clip(length[3]*self.size,0, 10))), 9, 9] = 1.0

        return np.clip(world, 0, 1)
