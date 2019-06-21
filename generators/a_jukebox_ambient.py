# modules
import numpy as np
from random import random, choice
from generators.g_cube import g_cube
from generators.g_blank import g_blank
from generators.g_torusrotation import g_torusrotation
from generators.g_growing_sphere import g_growing_sphere
from generators.g_rising_square import g_rising_square
from generators.g_rotating_cube import g_rotating_cube
from generators.g_random import g_random
from generators.g_drop import g_drop
from generators.g_corner_grow import g_corner_grow
from generators.g_cube_edges import g_cube_edges
from generators.g_cut import  g_cut

from effects.e_rainbow import e_rainbow
from effects.e_gradient import e_gradient
from effects.e_redyellow import e_redyellow
from effects.e_violetblue import e_violetblue

class a_jukebox_ambient():
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
        self.oldworld1 = np.zeros([3, 10, 10, 10])
        self.oldworld2 = np.zeros([3, 10, 10, 10])

        self.library = []
        self.library.append([['g_rotating_cube', 1.8/10.0, 3.15/10.0, 0.0], ['e_violetblue', 0.1, 0.0, 0.0], 1, 0.75, 0.2])
        self.library.append([['g_random', 0.1, 0.0, 0.0], ['e_violetblue', 0.03, 0.0, 0.0], 4, 0.9, 1.0])
        self.library.append([['g_drop', 0.3, 0.0, 0.0], ['e_gradient', 0.5, 0.06, 0.9], 1, 0.73, 1.0])
        self.library.append([['g_corner_grow', 17/50.0, 0.0, 0.0], ['e_redyellow', 0.2, 0.0, 0.0], 1, 0.8, 1.0])
        self.library.append([['g_cut', 0.09, 0.0, 0.0], ['e_violetblue', 0.1, 0.0, 0.0], 1, 0.5, 1.0])
        self.library.append([['g_random', 0.08, 0.0, 0.0], ['e_violetblue', 0.3, 0.0, 0.0], 4, 0.9, 1.0])
        self.library.append([['g_cube_edges', 0.6, 1.0, 0.0], ['e_rainbow', 0.3, 0.0, 0.0], 1, 0.8, 1.0])

        # ['generator, par1, par2, par3'], ['effect', par1, par2, par3], shutter, fade, brightness
#        self.library.append([['g_cube', 1.0, 0.5, 0.0], ['e_rainbow', 0.2, 0.0, 0.0], 10, 0.1, 1.0])
#        self.library.append([['g_torusrotation', 0.0, 0.0, 0.0], ['e_rainbow', 0.2, 0.0, 0.0], 1, 0.1, 1.0])
#        self.library.append([['g_growing_sphere', 0.5, 0.3, 0.0], ['e_rainbow', 0.2, 0.0, 0.0], 1, 0.1, 0.5])
#        self.library.append([['g_rising_square', 0.3, 0, 38/41.0], ['e_gradient', 0.66, 0.36, 0.8], 1, 0.65, 1.0])
        self.current1 = self.library[0]
        self.current2 = self.library[0]

        # load inital generator
        self.generator1 = eval(self.current1[0][0])()
        self.generator1.control(self.current1[0][1], self.current1[0][2], self.current1[0][3])

        # load initial effect
        self.effect1 = eval(self.current1[1][0])()
        self.effect1.control(self.current1[1][1], self.current1[1][2], self.current1[1][3])

        # load inital generator
        self.generator2 = eval(self.current2[0][0])()
        self.generator2.control(self.current2[0][1], self.current2[0][2], self.current2[0][3])

        # load initial effect
        self.effect2 = eval(self.current2[1][0])()
        self.effect2.control(self.current2[1][1], self.current2[1][2], self.current2[1][3])

    def control(self, counter1, counter2, blub2):
        self.change1 = int(counter1 * 200)
        self.change2 = int(counter2 * 200)

    def label(self):
        return ['Counter 1', self.change1,
                'Counter 2', self.change2,
                'empty', 'empty']

    def generate(self, step, dumpworld):
        world1 = np.zeros([3, 10, 10, 10])
        world2 = np.zeros([3, 10, 10, 10])

        if self.counter1 > self.change1:
            self.current = choice(self.library)

            # load inital generator
            self.generator1 = eval(self.current1[0][0])()
            self.generator1.control(self.current1[0][1], self.current1[0][2], self.current1[0][3])

            # load initial effect
            self.effect1 = eval(self.current1[1][0])()
            self.effect1.control(self.current1[1][1], self.current1[1][2], self.current1[1][3])
            self.counter1 = 0

        if self.counter2 > self.change2:
            self.current2 = choice(self.library)

            # load inital generator
            self.generator2 = eval(self.current2[0][0])()
            self.generator2.control(self.current2[0][1], self.current2[0][2], self.current2[0][3])

            # load initial effect
            self.effect2 = eval(self.current2[1][0])()
            self.effect2.control(self.current2[1][1], self.current2[1][2], self.current2[1][3])
            self.counter2 = 0


        if self.step % self.current1[2] == 0:
            world1 = self.generator1.generate(self.counter1, world1)
            world1 = self.effect1.generate(self.counter1, world1)

        if self.step % self.current2[2] == 0:
            world2 = self.generator2.generate(self.counter2, world2)
            world2 = self.effect2.generate(self.counter2, world2)

        world1 += self.oldworld1 * self.current1[3]
        world2 += self.oldworld2 * self.current2[3]
        self.oldworld1 = world1
        self.oldworld2 = world2

        self.step += 1
        self.counter1 += 1
        self.counter2 += 1

        return np.clip(world1*self.current1[4] + world2*self.current2[4], 0, 1)
