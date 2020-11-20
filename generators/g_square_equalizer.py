import numpy as np
from multiprocessing import shared_memory

class g_square_equalizer():

    def __init__(self):
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0

        self.amount = [0.5,0.5,0.5,0.5]

    def return_values(self):
        return [b'square_equalizer', b'amount 1', b'amount 2', b'amount 3', b'amount 4']

    def return_gui_values(self):

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.amount[0],2)),
                                                               str(round(self.amount[0],2)),
                                                               str(round(self.amount[0],2)),
                                                               str(round(self.amount[0],2))),'utf-8')

    def __call__(self, args):
        # get arguments
        for i in range(4):
            self.amount[i] = args[i]

        world = np.zeros([3, 10, 10, 10])

        # draw box
        for i in range(4):
            current_volume = np.clip(int(float(str(self.sound_values.buf[i*8:i*8+8],'utf-8'))*self.amount),0,9)

            world[:, current_volume, i:9-i, 0] = 1.0
            world[:, current_volume, i:9-i, 9] = 1.0
            world[:, current_volume, 0, i:9-i] = 1.0
            world[:, current_volume, 9, i:9-i] = 1.0

        return world
