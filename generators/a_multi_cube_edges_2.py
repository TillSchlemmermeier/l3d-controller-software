# modules
import numpy as np
from random import choice, uniform
from generators.g_genhsphere import gen_hsphere
from colorsys import rgb_to_hsv, hsv_to_rgb
from generators.g_cube_edges import g_cube_edges

class a_multi_cube_edges_2():

    def __init__(self):#
        self.counter = 0
        self.numbers = 1
        self.number = 1
        self.gens = []
        self.gens.append(g_cube_edges())
        self.gens.append(g_cube_edges())
        self.gens.append(g_cube_edges())
        self.gens.append(g_cube_edges())
        self.gens.append(g_cube_edges())
        self.gens.append(g_cube_edges())
        self.gens.append(g_cube_edges())
        self.gens.append(g_cube_edges())

    def control(self, *args):
        self.numbers = int(args[0]*7)+1
        self.number =  args[1]

    def label(self):
        return ['number of edges', self.numbers,
                'number of edge', int(3*self.number),
                'empty', 'empty']

    def generate(self, step, dumpworld):
        # create world
        for g in self.gens:
            g.control(1, self.number, 0)

        world = np.zeros([3, 10, 10, 10])
        for i in range(self.numbers):
            world += self.gens[i].generate(self.counter, world)

        self.counter += 1

        return np.clip(world, 0, 1)
