# modules
import numpy as np
from multiprocessing import shared_memory
from generators.gen_central_glow_f import gen_central_glow

class g_centralglow():
    def __init__(self):
        self.amount = 1.0
        # sound2light stuff
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 3
        self.size = 1

    #strings for GUI
    def return_values(self):
        return [b'centralglow', b'amount', b'', b'', b'channel']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.amount,2)), '', '', str(round(self.channel,1))), 'utf-8')

    def __call__(self, args):
        self.amount = args[0]*8
        self.channel = int(args[3]*3)

        current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
        self.size = current_volume * self.amount

        world[0, :, :, :] = gen_central_glow(self.size)
        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        return np.clip(world, 0, 1)
