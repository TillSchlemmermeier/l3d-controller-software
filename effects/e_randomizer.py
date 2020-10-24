# modules
import numpy as np
from multiprocessing import shared_memory

class e_randomizer():

    def __init__(self):
        self.amount = 0.5
        self.channel = 4
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

    def return_values(self):

        return [b'randomizer', b'amount', b'channel', b'', b'']

    def return_gui_values(self):
        if self.channel >= 0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.amount,1)), channel, '', ''), 'utf-8')

    def __call__(self, world, args):
        self.amount = args[0]
        self.channel = int(args[1]*4)-1

        if self.channel < 0 :
            r = np.random.normal(0, self.amount, [10,10,10])
        else:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            r = np.random.normal(0, np.clip(current_volume,0,10)*self.amount*2, [10,10,10])

        world[0, :, :, :] = world[0, :, :, :]+r*world[0, :, :, :]
        world[1, :, :, :] = world[1, :, :, :]+r*world[1, :, :, :]
        world[2, :, :, :] = world[2, :, :, :]+r*world[2, :, :, :]

        return np.clip(world, 0, 1)
