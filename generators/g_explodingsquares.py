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
        self.dir = 0
        '''
        self.axis = 1
        self.dir = 0
        self.inside = 0
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        '''
    def return_values(self):
        return [b'explodingsquares', b'direction', b'', b'', b'channel']

    def return_gui_values(self):
        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        if self.dir == 0:
            direction = 'X'
        elif self.dir == 1:
            direction = 'Y'
        else:
            direction ='Z'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(direction,'', '', channel),'utf-8')

    def __call__(self, args):
        self.direction = int(args[0]*3)
        self.channel = int(args[3]*4)-1

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
        self.xpos = randint(0,9)
        self.ypos = randint(0,9)
        self.zpos = randint(0,9)

        if self.counter < 10:
            if self.direction == 0:
                world[:, self.xpos, self.ypos - self.counter : self.ypos + self.counter, self.zpos - self.counter : self.zpos + self.counter] = 1
                world[:, self.xpos, self.ypos - self.counter + 1 : self.ypos + self.counter - 1, self.zpos - self.counter +1 : self.zpos + self.counter - 1] = 0

            elif self.direction == 1:
                world[:, self.xpos - self.counter : self.xpos + self.counter, self.ypos , self.zpos - self.counter : self.zpos + self.counter] = 1
                world[:, self.xpos - self.counter + 1: self.xpos + self.counter - 1, self.ypos , self.zpos - self.counter + 1: self.zpos + self.counter - 1] = 0

            else:
                world[:, self.xpos - self.counter : self.xpos + self.counter, self.ypos - self.counter : self.ypos + self.counter, self.zpos] = 1
                world[:, self.xpos - self.counter + 1: self.xpos + self.counter - 1, self.ypos - self.counter + 1: self.ypos + self.counter - 1, self.zpos] = 0

            self.counter += 1

        else:
            self.counter = 0

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
