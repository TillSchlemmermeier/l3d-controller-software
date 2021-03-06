# modules
import numpy as np
from generators.g_cube import g_cube

class a_testbot():
    '''
    Generator: Testbot
    '''

    def __init__(self):
        self.counter = 1

    def control(self, numbers, fade, blub1):
        pass

    def label(self):
        return ['empty', 'empty',
                'empty', 'empty',
                'empty', 'empty']

    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

        generator = g_cube()

        if self.counter <= 100:
            generator.control(1,1,0)
            self.counter += 1
        elif self.counter > 100 and self.counter <= 200:
            generator.control(0.5,1,0)
            self.counter += 1
        if self.counter > 200:
            self.counter = 0
        else:
            self.counter += 1

        world[:, :, :, :] = generator.generate(self.counter, 0)
        #world[1, :, :, :] = world[0, :, :, :]
        #world[2, :, :, :] = world[0, :, :, :]

        return np.clip(world, 0, 1)
