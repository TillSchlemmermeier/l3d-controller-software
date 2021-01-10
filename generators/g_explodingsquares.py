# modules
import numpy as np
from random import randint, choice
from multiprocessing import shared_memory

class g_explodingsquares():

    def __init__(self):

        # get initial random lines
        self.xpos = 1
        self.ypos = 1
        self.zpos = 1
        self.size = 1
        self.counter = 0
        self.direction = 0
        self.nframes = 6
        self.borders = 0
        '''
        self.axis = 1
        self.dir = 0
        self.inside = 0
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        '''
    def return_values(self):
        return [b'explodingsquares', b'borders', b'', b'', b'channel']

    def return_gui_values(self):
        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        if self.borders <= 0.5:
            borders = 'off'
        else:
            borders = 'on'


        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(borders,'', '', channel),'utf-8')

    def __call__(self, args):
        self.borders = args[0]
        self.channel = int(args[3]*4)-1

        if args[0] <= 0.5:
            borders = [0,10]
        else:
            borders = [1,9]

        world = np.zeros([3, 10, 10, 10])
        '''
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
        '''



        if self.counter <= self.nframes:
            world[:, self.xpos, np.clip(self.ypos - self.counter,0,9) : self.ypos + self.counter, np.clip(self.zpos - self.counter,0,9) : self.zpos + self.counter] = 1
            world[:, self.xpos, np.clip(self.ypos - self.counter + 1,borders[0],9) : np.clip(self.ypos + self.counter - 1,-2,borders[1]), np.clip(self.zpos - self.counter + 1,borders[0],9) : np.clip(self.zpos + self.counter - 1,-2, borders[1])] = 0

            if self.direction == 1:
                world[0, :, :, :] = np.rot90(world[0, :, :, :], 1, axes = (0, 1))
            elif self.direction == 2:
                world[0, :, :, :] = np.rot90(world[0, :, :, :], 1, axes = (0, 2))

            self.counter += 1
            world[1, :, :, :] = world[0, :, :, :]
            world[2, :, :, :] = world[0, :, :, :]

        else:
            self.counter = 0
            self.xpos = randint(3,6)
            self.ypos = randint(3,6)
            self.zpos = randint(3,6)
            self.direction = randint(0,3)

            if self.direction == 0:
                if 4 < self.zpos < 7 and 4 < self.ypos < 7:
                    self.nframes = 7
                else:
                    self.nframes = 7
            elif self.direction == 1:
                if 4 < self.xpos < 7 and 4 < self.zpos < 7:
                    self.nframes = 7
                else:
                    self.nframes = 7
            else:
                if 4 < self.zpos < 7 and 4 < self.ypos < 7:
                    self.nframes = 7
                else:
                    self.nframes = 7


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
