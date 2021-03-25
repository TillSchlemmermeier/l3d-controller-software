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
        self.nframes = 7
        self.borders = 0
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.trigger = False
        self.lastvalue = 0


    def return_values(self):
        return [b'explodingsquares', b'borders', b'', b'', b'Trigger']

    def return_gui_values(self):
        if self.trigger:
            trigger = 'On'
        else:
            trigger = 'Off'

        if self.borders <= 0.5:
            borders = 'off'
        else:
            borders = 'on'


        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(borders,'', '', trigger),'utf-8')

    def __call__(self, args):
        self.borders = args[0]

        if args[3] > 0.5:
            self.trigger = True
        else:
            self.trigger = False

        if args[0] <= 0.5:
            borders = [0,10]
        else:
            borders = [1,9]

        world = np.zeros([3, 10, 10, 10])

        # check if trigger is activated
        if self.trigger:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = 0
                self.xpos = randint(3,6)
                self.ypos = randint(3,6)
                self.zpos = randint(3,6)
                self.direction = randint(0,3)
            if self.counter > 8:
                self.counter = 8


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

        elif not self.trigger:
            self.counter = 0
            self.xpos = randint(3,6)
            self.ypos = randint(3,6)
            self.zpos = randint(3,6)
            self.direction = randint(0,3)

        return np.round(np.clip(world, 0, 1), 3)
