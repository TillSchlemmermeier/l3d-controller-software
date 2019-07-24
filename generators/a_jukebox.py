# modules
import numpy as np
from random import random, choice
from generators.g_cube import g_cube
from generators.g_blank import g_blank
from generators.g_torusrotation import g_torusrotation
from generators.g_growing_sphere import g_growing_sphere
from generators.g_rising_square import g_rising_square
from generators.g_blackhole import g_blackhole
from generators.g_growing_corner import g_growing_corner
from generators.g_randomlines import g_randomlines
from generators.g_growingface import g_growingface

from effects.e_rainbow import e_rainbow
from effects.e_gradient import e_gradient
class a_jukebox():
    '''
    '''

    def __init__(self):

        # create step counter
        self.step = 0
        self.counter1 = 0
        self.counter2 = 0
        self.change1 = 100
        self.change2 = 100

        # write old world
        self.oldworld = np.zeros([3, 10, 10, 10])

        self.library = []
        # ['generator, par1, par2, par3'], ['effect', par1, par2, par3], shutter, fade, brightness
        self.library.append([['g_cube', 1.0, 0.5, 0.0], ['e_rainbow', 0.2, 0.0, 0.0], 10, 0.1, 1.0])
        self.library.append([['g_torusrotation', 0.0, 0.0, 0.0], ['e_rainbow', 0.2, 0.0, 0.0], 1, 0.1, 1.0])
        self.library.append([['g_growing_sphere', 0.5, 0.3, 0.0], ['e_rainbow', 0.2, 0.0, 0.0], 1, 0.1, 0.5])
        self.library.append([['g_rising_square', 0.3, 0, 38/41.0], ['e_gradient', 0.66, 0.36, 0.8], 1, 0.65, 1.0])
        self.library.append([['g_blackhole',0.67, 0.18/0.55, 0.0], ['e_rainbow', 1.0, 0.0, 0.0], 1.0, 0.8, 0.7])
        self.library.append([['g_growing_corner', 17/18.0, 11.2/60.0, 0.0], ['e_rainbow', 0.44/1.5, 0.0, 0.0], 1, 0.8, 0.65])
        self.library.append([['g_randomlines', 17/18.0, 11.2/60.0, 0.0], ['e_rainbow', 0.44/1.5, 0.0, 0.0], 3, 0.7, 1.0])
        self.library.append([['g_growingface', 0.8/18.0, 0.1, 0.0], ['e_rainbow', 0.44/1.5, 0.0, 0.0], 1, 0.7, 1.0])

        self.current = self.library[0]

        # load inital generator
        self.generator = eval(self.current[0][0])()
        self.generator.control(self.current[0][1], self.current[0][2], self.current[0][3])

        # load initial effect
        self.effect = eval(self.current[1][0])()
        self.effect.control(self.current[1][1], self.current[1][2], self.current[1][3])

    def control(self, counter1, counter2, blub2):
        self.change1 = int(counter1 * 500)+50
        self.change2 = int(counter2 * 500)+50

    def label(self):
        return ['Counter 1', self.change1,
                'Counter 2', self.change2,
                'empty', 'empty']

    def generate(self, step, dumpworld):
        world = np.zeros([3, 10, 10, 10])

        if self.counter1 > self.change1:
            self.current = choice(self.library)

            # load inital generator
            self.generator = eval(self.current[0][0])()
            self.generator.control(self.current[0][1], self.current[0][2], self.current[0][3])

            # load initial effect
            self.effect = eval(self.current[1][0])()
            self.effect.control(self.current[1][1], self.current[1][2], self.current[1][3])
            self.counter1=0


        if self.step % self.current[2] == 0:
            world = self.generator.generate(self.step, world)
            world = self.effect.generate(self.step, world)

        world += self.oldworld * self.current[3]
        self.oldworld = world
        self.step += 1
        self.counter1 += 1
        return np.clip(world*self.current[4], 0, 1)
