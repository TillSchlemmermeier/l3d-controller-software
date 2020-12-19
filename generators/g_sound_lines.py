# modules
import numpy as np
from random import randint
from multiprocessing import shared_memory


class g_sound_lines():

    def __init__(self):

        # get initial random lines
        self.lines = []
        for i in range(10):
            self.lines.append([slice(0, 10, 1), randint(0, 9), randint(0, 9)])

        self.counter = 1
        self.reset = 20
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")


    def return_values(self):
        return [b'sound_lines', b'reset', b'', b'', b'channel']


    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.reset,2)), '', '', str(round(self.channel,2))),'utf-8')


    def __call__(self, args):

        # process parameters
        self.reset = args[0]*20+1
        self.channel = int(args[3]*3)

        current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
        # now we can world with the sound
        world = np.zeros([3, 10, 10, 10])

        # get lines
        for line in self.lines:
                world[0, line[0], line[1], line[2]] = current_volume

        # copy to other colors
        world[1:, :, :, :] = world[0, :, :, :]
        world[2:, :, :, :] = world[0, :, :, :]

        if self.counter > self.reset:
            self.lines = []
            # reset lines
            for i in range(10):
                self.lines.append([slice(0, 10, 1), randint(0, 9), randint(0, 9)])

            self.counter = 0

        self.counter += 1

        return np.round(np.clip(world, 0, 1), 3)
