# modules
import numpy as np
from generators.g_orbiter import g_orbiter

class a_orbbot():
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

        generator = g_orbiter()

        generator.control(0.5*(np.sin(self.counter * 0.01)*0.5+0.5),0.4,0.05)

        world[:, :, :, :] = generator.generate(self.counter, 0)

        self.counter += 1

        return np.clip(world, 0, 1)
