# modules
import numpy as np
from random import choice


class g_cube_edges():
    '''
    Generator: cube_edges

    selects a random edge and propagates
    a bright spot along the edge.

    TODO: direction!
    '''

    def __init__(self):
        self.counter = 20
        self.speed = 1
        self.number = 1
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
        self.direction = choice([-1, 1])


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

        # check for new spawn
        if self.counter > 19:
            self.counter = 0
            # select new edge and direction
            self.edge = choice(self.edge_list)
            self.direction = choice([-1, 1])

        # generate vector with values
        row = np.linspace(0, 19, 20)
        row = np.exp(-np.abs(row - self.counter))

        # copy middle of the vector to world
        if self.direction == 1:
            world[0, self.edge[0], self.edge[1], self.edge[2]] = row[5:15]
        else:
            world[0, self.edge[0], self.edge[1], self.edge[2]] = row[5:15][::-1]

        if self.number == 2:
            if self.direction == 1:
                world[0, self.edge[1], self.edge[2], self.edge[0]] = row[5:15]
            else:
                world[0, self.edge[1], self.edge[2], self.edge[0]] = row[5:15][::-1]
                
        if self.number == 3:
            if self.direction == 1:
                world[0, self.edge[2], self.edge[0], self.edge[1]] = row[5:15]
            else:
                world[0, self.edge[2], self.edge[0], self.edge[1]] = row[5:15][::-1]
                
        # increase counter
        self.counter += self.speed

        # brightness : x**3 for linear change
        # see https://de.wikipedia.org/wiki/Stevenssche_Potenzfunktion

        # copy world together
        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        return np.clip(world, 0, 1)
