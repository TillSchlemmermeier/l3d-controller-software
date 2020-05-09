# modules
import numpy as np
from random import choice
from generators.g_cube import g_cube
from generators.g_blank import g_blank

class a_lines():
    '''
    Automat: lines

    fades in random edges, and at some
    point do some strobo with the cube
    '''

    def __init__(self):
        self.counter = 0

	    # counter for changes
        self.start_strobo = 4
        self.count_strobo = 20
        self.count_fade = 100

        # initialize generator
        self.generator = g_cube()
        # self.generator.control(1,1,0)

        self.edge_list = [[0, 0, slice(0, 10)],
                          [0, 9, slice(0, 10)],
                          [9, 0, slice(0, 10)],
                          [9, 9, slice(0, 10)],
                          [0, slice(0, 10), 0],
                          [0, slice(0, 10), 9],
                          [9, slice(0, 10), 0],
                          [9, slice(0, 10), 9],
                          [slice(0, 10), 0, 0],
                          [slice(0, 10), 0, 9],
                          [slice(0, 10), 9, 0],
                          [slice(0, 10), 9, 9],
                          ]
        self.edge = choice(self.edge_list)

    #Strings for GUI
    def return_values(self):
        return [b'a_lines', b'count_fade', b'', b'', b'']

    def __call__(self, args):
        self.count_fade = int(args[0] * 200)+50

        # create world
        world = np.zeros([3, 10, 10, 10])

        # select new edge after self.count_fade
        if self.counter % self.count_fade == 0:
            self.edge = choice(self.edge_list)

        # calculate brightness and turn on edge
        brightness = np.sin(self.counter/self.count_fade*np.pi)**6
        world[:, self.edge[0], self.edge[1], self.edge[2]] = brightness

        # do strobo with cube
        if self.counter > self.start_strobo*self.count_fade:
            if self.counter % 2 == 0:
                world[:, :, :, :] = self.generator(self.counter,0)

        if self.counter > self.count_strobo+self.start_strobo*self.count_fade:
            self.counter = -1

        self.counter += 1

        return np.clip(world, 0, 1)
