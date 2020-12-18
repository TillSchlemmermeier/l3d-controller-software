# modules
import numpy as np
from multiprocessing import shared_memory

class g_edgelines():

    def __init__(self):
        self.counter = 0
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0


    def return_values(self):
        # Strings for GUI
        return [b'edgelines', b'', b'', b'', b'channel']

    def return_gui_values(self):
        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format('', '', '', channel),'utf-8')


    def __call__(self, args):
        self.channel = int(args[3]*4)-1

        world = np.zeros([3, 10, 10, 10])

        # check if S2L is activated
        if self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume <= 0:
                self.counter = round(self.counter-0.5)
                self.counter *= 10

        # down
        if self.counter <= 10:
            world[:, :self.counter, 0, 0] = 1.0
            world[:, :self.counter, 9, 9] = 1.0
        elif self.counter > 10 and self.counter <= 20:
            world[:, self.counter-10:, 0, 0] = 1.0
            world[:, self.counter-10:, 9, 9] = 1.0
        # side
        elif self.counter > 20 and self.counter <= 30:
            world[:, 9, :self.counter-30, 0] = 1.0
            world[:, 9, 0, :self.counter-30] = 1.0
            world[:, 9, 10-(self.counter-20):, 9] = 1.0
            world[:, 9, 9, 10-(self.counter-20):] = 1.0
        elif self.counter > 30 and self.counter <= 40:
            world[:, 9, self.counter-31:, 0] = 1.0
            world[:, 9, 0, self.counter-31:] = 1.0
            world[:, 9, :9-(self.counter-20), 9] = 1.0
            world[:, 9, 9, :9-(self.counter-20)] = 1.0
        # up
        elif self.counter > 40 and self.counter <= 50:
            world[:, 10-(self.counter-40):, 9, 0] = 1.0
            world[:, 10-(self.counter-40):, 0, 9] = 1.0
        elif self.counter > 50 and self.counter <= 60:
            world[:, :10-(self.counter-50), 9, 0] = 1.0
            world[:, :10-(self.counter-50), 0, 9] = 1.0
        # side
        elif self.counter > 60 and self.counter <= 70:
            world[:, 0, 0, 10-(self.counter-60):] = 1.0
            world[:, 0, 10-(self.counter-60):, 0] = 1.0
            world[:, 0, :self.counter-60, 9] = 1.0
            world[:, 0, 9, :self.counter-60] = 1.0
        elif self.counter > 70 and self.counter <= 80:
            world[:, 0, 0, :9-(self.counter-60)] = 1.0
            world[:, 0, :9-(self.counter-60), 0] = 1.0
            world[:, 0, self.counter-70:, 9] = 1.0
            world[:, 0, 9, self.counter-70:] = 1.0
        else:
            self.counter = -1

        self.counter += 1

        return np.clip(world, 0, 1)
