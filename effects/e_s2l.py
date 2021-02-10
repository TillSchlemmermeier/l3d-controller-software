
import numpy as np
from multiprocessing import shared_memory

class e_s2l():


    def __init__(self):
        # parameters
        self.amount = 1.0
        self.channel = 1.0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.lastvalue = 0
        self.counter = 0
        self.step = 8

    def return_values(self):
        # strings for GUI
        return [b's2l', b'amount', b'channel', b'', b'']

    def return_gui_values(self):
        if self.channel < 4:
            channel = str(self.channel)
        else:
            channel = "Trigger"

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.amount,1)), channel, '','') ,'utf-8')

    def __call__(self, world, args):
        # process parameters
        self.amount = args[0]
        self.channel = int(args[1]*4)

        # apply manipulation
        if self.channel < 4:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))**4
            #for i in range(3):
            #    world[i, :, :, :] *= (1-self.amount) + np.clip(current_volume,0,1)*self.amount

            # maybe edit formula?
            world[:, :, :, :] *= (1-self.amount) + np.clip(current_volume,0,1)*self.amount

        else:
            current_volume = int(float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = 0

            # maybe more than 8:
            if self.counter < self.step:
                world[:, :, :, :] *= (1 - self.amount) + ((self.step - self.counter) / self.step) * self.amount

            self.counter += 1

        return np.clip(world, 0, 1)
