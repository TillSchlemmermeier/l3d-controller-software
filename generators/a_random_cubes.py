# modules
import numpy as np
from random import random
from generators.g_cube import g_cube
from generators.g_blank import g_blank

class a_random_cubes():
    '''
    '''

    def __init__(self):
        self.counter = 0
        # counter for changes
        self.count_strobo = 20
        self.count_wait = 100

        self.state = 'wait'

        # initialize generator
        self.generator = g_cube()
        self.generator.control(1,1,0)

    def control(self, count_wait, count_strobo, blub1):
        self.count_wait = int(count_wait * 200)+50
        self.count_strobo = int(count_strobo*20)+5

    def label(self):
        return ['count wait', self.count_wait,
                'count strobo', self.count_strobo,
                'empty', 'empty']

    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

        if self.state == 'wait':
            self.counter += 1
            if self.counter >= self.count_wait:
                self.state = 'strobo'
                self.counter = 0

        elif self.state == 'strobo':
            self.generator.control(random(),1,0)
            world[:,:,:,:] = self.generator.generate(self.counter, 0)
            self.counter += 1
            if self.counter >= self.count_strobo:
                self.state = 'wait'
                self.counter = 0

        return np.clip(world, 0, 1)
