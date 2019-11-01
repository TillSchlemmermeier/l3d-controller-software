# modules
import numpy as np
from random import randint
from convert2d import convert2d

class g_2d_random_inner_square():

    def __init__(self):

    def control(self, waiting frames, blub1, blub2):
        pass

    def label(self):
        return ['empty', 'empty', 'empty', 'empty', 'empty', 'empty']

    def generate(self, step, dumpworld):

        world_2d = np.zeros([3, 20, 40])

        size = randint(0, 4)

        # turn on till maximum size
        world[:, size: 9-size, size*2:19-size*2] = 1.0

        # delete inner
        world[:, size+1: 8-size, size*2+2:17-size*2] = 0.0

        # delete sides
        world[:,10:, :] = 0.0
        world[:,:, :10] = 0.0
        world[:,:, 30] = 0.0


        world = convert2d(world_2d)

        return np.clip(world, 0, 1)
