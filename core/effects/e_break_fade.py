
import numpy as np
from multiprocessing import shared_memory

class e_break_fade():

    def __init__(self):
        # parameters
        self.amount = 1.0
        self.channel = 1
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.lastworld = np.zeros([3,10,10,10])
        self.counter = 0
        self.countermax = 0
        self.invert = True

    def return_state(self):
        return []

    def __call__(self, world, args):

        current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))

        if self.invert:
            newlength = np.clip(int(7 * (current_volume) * self.amount), 0.01, 10)

            if newlength < self.counter:
                self.counter = 0
                self.countermax = newlength

            for i in range(3):
                world[i, :, :, :] += (0.9-(self.counter)/(self.countermax+0.001))*self.lastworld[i, :, :, :]
                self.lastworld[i, :, :, :] = np.clip(world[i, :, :, :], 0, 1)

            self.counter += 1


        else:
            newlength = int(10 * current_volume * self.amount)

            if newlength > self.counter:
                # triggered, if sound is louder than counter
                # -> reset counter
                self.counter = newlength
                self.countermax = self.counter

            for i in range(3):
                world[i, :, :, :] += ((self.counter)/(self.countermax + 1 ))*self.lastworld[i, :, :, :]
                self.lastworld[i, :, :, :] = np.clip(world[i, :, :, :], 0, 1)

            if self.counter > 0:
                self.counter -= 1

        return np.clip(world, 0, 1)
