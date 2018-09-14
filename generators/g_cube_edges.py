# modules
import numpy as np
from random import choice, seed


class g_cube_edges():
    '''
    Generator: cube_edges

    selects a random edge and propagates
    a bright spot along the edge.

    '''

    def __init__(self):
        self.counter = 20
        self.speed = 1
        self.number = 1
        # corner_list contains the indices for edges
        # which belong to one corner
        self.corner_list = [[   0, 8, 4], # A
                            [-0.1, 5, 9], # B
                            [   6, 2,-8], # C
                            [  -9,-2, 7], # D
                            [   1,10,-4], # E
                            [11, -5, -1], # F
                            [ 3, -6,-10], # G
                            [-11,-3, -7]] # H
        '''
        E - - F
        |\    |\
        | A - - B
        G | - H |
         \|    \|
          C - - D
        '''

        self.edge_list = [[0, 0, slice(0, 10)], #  0
                          [0, 9, slice(0, 10)], #  1
                          [9, 0, slice(0, 10)], #  2
                          [9, 9, slice(0, 10)], #  3
                          [0, slice(0, 10), 0], #  4
                          [0, slice(0, 10), 9], #  5
                          [9, slice(0, 10), 0], #  6
                          [9, slice(0, 10), 9], #  7
                          [slice(0, 10), 0, 0], #  8
                          [slice(0, 10), 0, 9], #  9
                          [slice(0, 10), 9, 0], # 10
                          [slice(0, 10), 9, 9], # 11
                          ]

        self.corner = self.corner_list[0] # choice(self.corner_list)
        self.direction = choice([-1, 1])
        seed()


    def control(self, speed, number, blub1):
        self.speed = speed
        self.number = int(3*number)
        if self.number == 0:
            self.number = 1

    def label(self):
        return ['speed', round(self.speed, 2),
                'number', self.number,
                'empty', 'empty']

    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

        # choose new corner
        if self.counter > 19:
            self.counter = 0
            self.corner = choice(self.corner_list)

        # create gaussian profile
        row = np.linspace(0, 19, 20)
        row = np.exp(-np.abs(row - self.counter))

        # first edge
        edge1 = self.edge_list[int(abs(self.corner[0]))]
        if self.corner[0] >= 0:
            world[0, edge1[0], edge1[1], edge1[2]] = row[5:15]
        else:
            world[0, edge1[0], edge1[1], edge1[2]] = row[5:15][::-1]

        # second edge
        if self.number > 1:
            edge2 = self.edge_list[int(abs(self.corner[1]))]
            if self.corner[1] >= 0:
                world[0, edge2[0], edge2[1], edge2[2]] = row[5:15]
            else:
                world[0, edge2[0], edge2[1], edge2[2]] = row[5:15][::-1]

        if self.number > 2:
            edge3 = self.edge_list[int(abs(self.corner[2]))]
            if self.corner[2] >= 0:
                world[0, edge3[0], edge3[1], edge3[2]] = row[5:15]
            else:
                world[0, edge3[0], edge3[1], edge3[2]] = row[5:15][::-1]

        # increase counter
        self.counter += self.speed

        # brightness : x**3 for linear change
        # see https://de.wikipedia.org/wiki/Stevenssche_Potenzfunktion

        # copy world together
        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        return np.clip(world, 0, 1)
