# modules
import numpy as np
from generators.g_pyramid import g_pyramid
from generators.g_pyramid_upsidedown import g_pyramid_upsidedown
from generators.g_cube import g_cube
from generators.g_blank import g_blank

class a_lines():
    '''
    Generator: Testbot
    '''

    def __init__(self):
        self.counter = 0
        self.generator = g_pyramid_upsidedown()
        self.generator.control(0,0.1,0)
        self.stopcounter = 200

    def control(self, numbers, fade, blub1):
        pass

    def label(self):
        return ['empty', 'empty',
                'empty', 'empty',
                'empty', 'empty']

    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

        if self.counter == 0:
            self.generator = g_pyramid_upsidedown()
            self.generator.control(0.0,0.1,0)

        if self.counter == self.stopcounter:
            self.generator = g_pyramid()
            self.generator.control(0.0,0.1,0)

        if self.counter == 2*self.stopcounter:
            self.generator = g_cube()
            self.generator.control(1,1,0)

        if self.counter == 2*self.stopcounter+1:
            self.generator = g_blank()
            self.generator.control(1,1,0)

        if self.counter == 2*self.stopcounter+2:
            self.generator = g_cube()
            self.generator.control(1,1,0)

        if self.counter == 2*self.stopcounter+3:
            self.counter = -1

        brightness = np.abs(np.sin(self.counter/self.stopcounter*np.pi))*0.7
        world[:, :, :, :] = brightness * self.generator.generate(self.counter, 0)

        self.counter += 1

        return np.clip(world, 0, 1)
