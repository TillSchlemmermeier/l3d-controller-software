# modules
import numpy as np
from random import choice, randint
from multiprocessing import shared_memory
from functools import partial

class g_meet_lines():

    def __init__(self):
        self.number = 0.1
        self.speed = 100

        # list of runnters
        self.runners = []
        for i in range(100):
            self.runners.append(runner())

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
        pos = []
        for i in range(self.number):
            pos.append(self.runners[i].run())
            world[0, pos[-1][0], pos[-1][1], pos[-1][2]] = 0.5

        pos = np.array(pos)

        # detect for x
        for ax in [[0,1], [0,2], [1,2]]:
            for i in range(self.number):
                for j in range(i+1, self.number):
                    if pos[i, ax[0]] == pos[j, ax[0]] and pos[i, ax[1]] == pos[j, ax[1]]:
                        if ax == [0, 1]:
                            world[:, pos[i,ax[0]], pos[i,ax[1]], :] = 1
                        elif ax == [0, 2]:
                            world[:, pos[i,ax[0]], : , pos[i,ax[1]]] = 1
                        else:
                            world[:, :, pos[i,ax[0]], pos[i,ax[1]]] = 1


        #world[1, :, :, :] = world[0, :, :, :]
        #world[2, :, :, :] = world[0, :, :, :]

        return np.clip(world, 0, 1)

class runner:

    def __init__(self):
        self.pos = [randint(1,8), randint(1,8), randint(1,8)]
        self.ax = randint(0, 2)
        self.dir = choice([0, 9])
        self.pos[self.ax] = self.dir
        self.state = 'run'

        if dir == 0:
            self.dir = 1
        else:
            self.dir = -1

    def reset(self):
        self.pos = [randint(1,8), randint(1,8), randint(1,8)]
        self.ax = randint(0, 2)
        dir = choice([0, 9])
        self.pos[self.ax] = dir
        self.state = 'run'

        if dir == 0:
            self.dir = 1
        else:
            self.dir = -1

    def run(self):

        # do things
        temp =  self.pos
        self.pos[self.ax] += self.dir

        # reset if at the end
        if self.pos[self.ax] <= 0 or self.pos[self.ax] >= 9:
            self.reset()

        return temp
