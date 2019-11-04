# modules
import numpy as np
from random import randint
from generators.convert2d import convert2d

class g_2d_random_inner_square():

    def __init__(self):
        pass

    def control(self, blub0, blub1, blub2):
        pass

    def label(self):
        return ['empty', 'empty', 'empty', 'empty', 'empty', 'empty']

    def generate(self, step, dumpworld):

        world_2d = np.zeros([3, 20, 40])

        size = randint(0, 4)

        # turn on till maximum size
        world_2d[:, size: 10-size, 10+size:30-size] = 1.0

        # delete inner
        if size < 4:
            world_2d[:, size+1: 9-size, 10+size+1:29-size] = 0.0

        # delete sides
        world_2d[:,10:, :] = 0.0
        world_2d[:,:, :10] = 0.0
        world_2d[:,:, 30:] = 0.0


        world = convert2d(world_2d)

        return np.clip(world, 0, 1)
