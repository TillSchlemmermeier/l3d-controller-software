# modules
import numpy as np
from generators.convert2d import convert2d

class g_2d_test():

    def __init__(self):
        pass

    def control(self, blub0, blub1, blub2):
        pass

    def label(self):
        return ['empty', 'empty', 'empty', 'empty', 'empty', 'empty']

    def generate(self, step, dumpworld):

        world_2d = np.zeros([3, 20, 40])

        world_2d[:, 0, :] = 1.0
        world_2d[:,-1, :] = 1.0
        world_2d[:, :, 0] = 1.0
        world_2d[:, :,-1] = 1.0

#        world_2d[0, :, 0] = 1.0
#        world_2d[1, :, 10] = 1.0
#        world_2d[2, :, 20] = 1.0
#        world_2d[0, :, 30] = 1.0

        for i in range(20):
            world_2d[0, i, i] = 1.0
            world_2d[0, i, i+20] = 1.0


        world_2d[1, 3, 2] = 1.0
        world_2d[1, 13, 12] = 1.0

        world = convert2d(world_2d)

        return np.clip(world, 0, 1)
