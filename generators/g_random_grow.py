# modules
import numpy as np
from random import randint, choice
from multiprocessing import shared_memory

class g_random_grow():

    def __init__(self):
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.world = np.zeros(10, 10, 10)
        self.number = 2

    #Strings for GUI
    def return_values(self):
        return [b'random grow', b'', b'', b'', b'channel']

    def return_gui_values(self):

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format('', '', '', ''),'utf-8')


    def __call__(self, args):
        self.number = int(args[0]*20)+1

        for i in range(self.number):
            self.world[randint(0,9), randint(0,9), randint(0,9)] += choice([-0.5, 0.5])

        # clip
        self.world = np.clip(self.world, 0, 1)

        # increase
        self.world *= 1.2

        # delete if necessary
        self.world[np.where(self.world > 0.95)] = 0

        # create final world
        world = np.zeros([3, 10, 10, 10])
        for i in range(3):
            world[i, :, :, :] = self.world

        return np.clip(world, 0, 1)
