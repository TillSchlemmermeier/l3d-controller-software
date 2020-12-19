# modules
import numpy as np
from random import randint, choice
from multiprocessing import shared_memory

class g_sidesquares():

    def __init__(self):

        # get initial random lines
        self.counter = 5
        self.axis = 1
        self.dir = 0
        self.inside = 0
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0

    def return_values(self):
        return [b'sidesquares', b'inside', b'', b'', b'channel']

    def return_gui_values(self):
        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(self.inside),'', '', channel),'utf-8')

    def __call__(self, args):
        self.inside = int(round(args[0]))
        self.channel = int(args[3]*4)-1

        world = np.zeros([3, 10, 10, 10])

        # check if S2L is activated
        if self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                world[0, :, :, :] = self.gen_slice(self.axis, self.dir, self.counter)

        else:
            world[0, :, :, :] = self.gen_slice(self.axis, self.dir, self.counter)

        # copy to other colors
        world[1:, :, :, :] = world[0, :, :, :]
        world[2:, :, :, :] = world[0, :, :, :]

        if self.counter <= 0:
            if self.inside == 0:
                self.dir = choice([0, 9])
            else:
                self.dir = randint(0, 9)

            self.axis = randint(0, 2)
            self.counter = 5

        self.counter -= 1

        return np.round(np.clip(world, 0, 1), 3)

    def gen_slice(self, axis, dir, size):

        side = np.zeros([10, 10])
        world = np.zeros([10, 10, 10])

        side[0+size : 10-size, size] = 1
        side[0+size : 10-size, 9-size] = 1
        side[size, 0+size : 10-size] = 1
        side[9-size, 0+size : 10-size] = 1

        if axis == 0:
            world[dir, :, :] = side[:, :]
        elif axis == 1:
            world[:, dir, :] = side[:, :]
        elif axis == 2:
            world[:, :, dir] = side[:, :]

        return world
