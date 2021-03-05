# modules
import numpy as np
from random import choice
from multiprocessing import shared_memory

class g_meet_lines():

    def __init__(self):
        self.number = 0.1
        self.speed = 100

        # list of runnters
        self.runnters = []
        for i in range(100):
            self.runners.append(runnter)

        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0

    #Strings for GUI
    def return_values(self):
        return [b'meet_lines', b'number', b'speed', b'', b'channel']

    def return_gui_values(self):
        if 4 > self.channel >= 0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = "Trigger"
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.number,2)), str(round(self.speed,2)), '', channel),'utf-8')

    def __call__(self, args):
        self.number = int(args[0]*50 + 1)
        self.speed = args[1]*0.5 + 0.1
        self.channel = int(args[3]*5)-1

        # create world
        world = np.zeros([3, 10, 10, 10])

        # run runners
        for i in range(number):
            pos = self.runnters[i]()
            world[0, pos[0], pos[1], pos[2]] = 1

        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        return np.clip(world, 0, 1)

class runner:

    def __init__(self):
        self.pos = [randint(1,8), randint(1,8), randint(1,8)]
        ax = randint(0, 2)
        dir = choice([0, 9])
        self.pos[ax] = dir
        self.state = 'run'

        if dir == 0:
            self.dir = 1
        else:
            self.dir = -1

    def reset(self):
        self.pos = [randint(1,8), randint(1,8), randint(1,8)]
        ax = randint(0, 2)
        dir = choice([0, 9])
        self.pos[ax] = dir
        self.state = 'run'

        if dir == 0:
            self.dir = 1
        else:
            self.dir = -1

    def __call__(self):

        # do things
        temp =  self.pos
        self.pos[self.ax] += self.dir

        # reset if at the end
        if self.pos[self.ax] < 0 or self.pos[self.ax] > 9:
            self.reset()
