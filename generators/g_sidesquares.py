# modules
import numpy as np
from random import randint, choice
from multiprocessing import shared_memory

class g_sidesquares():

    def __init__(self):
        # get initial random lines
        self.lines = []
        for i in range(10):
            self.lines.append(self.gen_slice(randint(0,2), randint(0,1), randint(0,4)))
        self.counter = 5
        self.axis = 1
        self.dir = 0
        self.inside = 0
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0
        self.steps = 0
        self.reset = 0
        self.number = 0

    def return_values(self):
        if self.channel < 0:
            return [b'sidesquares', b'inside', b'', b'', b'channel']
        else:
            return [b'sidesquares', b'inside', b'reset', b'number', b'channel']

    def return_gui_values(self):
        if 4 > self.channel >= 0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = "Trigger"
        else:
            channel = 'noS2L'

        if self.inside == 0:
            inside = 'Off'
        else:
            inside = 'On'

        if self.channel < 0:
            return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(inside,'', '', channel),'utf-8')
        else:
            return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(inside,str(self.reset), str(self.number), channel),'utf-8')

    def __call__(self, args):
        self.inside = int(round(args[0]))
        self.reset = int(args[1]*9+1)
        self.number = int(args[2]*12 + 1)
        self.channel = int(args[3]*5)-1

        world = np.zeros([3, 10, 10, 10])

        # check if S2L is activated
        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            # get lines
            for i in range(len(self.lines)):
                if current_volume > i*0.1:
                    world[0, :, :, :] += self.lines[i]*(current_volume-i*0.1)

        #check for trigger
        elif self.channel == 4:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.steps = self.reset

            if self.steps > 0:
                if self.counter <= 0:
                    if self.inside == 0:
                        self.dir = choice([0, 9])
                    else:
                        self.dir = randint(0, 9)

                    self.axis = randint(0, 2)
                    self.counter = 5

                world[0, :, :, :] = self.gen_slice(self.axis, self.dir, self.counter)
                self.counter -= 1
                self.steps -= 1


        else:
            world[0, :, :, :] = self.gen_slice(self.axis, self.dir, self.counter)

        # copy to other colors
        world[1:, :, :, :] = world[0, :, :, :]
        world[2:, :, :, :] = world[0, :, :, :]


        if 4 > self.channel >= 0:
            if self.counter > self.reset:
                self.lines = []
                # reset lines
                for i in range(self.number):
                    if self.inside == 0:
                        self.dir = choice([0, 9])
                    else:
                        self.dir = randint(0, 9)

                    self.lines.append(self.gen_slice(randint(0,2), self.dir, randint(0,4)))

                self.counter = 0

            self.counter += 1

        elif self.channel < 0:
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
