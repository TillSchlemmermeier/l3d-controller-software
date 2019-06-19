# modules
import numpy as np
from random import randint


class g_growing_square():
    def __init__(self):
        self.state = 0

        # choose random point and plane
        self.point = [randint(0, 9), randint(0, 9), randint(0, 9)]
        self.direction = randint(0, 2)

        # define color modes
        self.colormodes = {}
        self.colormodes[0] = ['white', [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]
        self.colormodes[1] = ['blue to orange', [0.0, 0.0, 1.0], [1.0, 0.5, 0.0]]

        # define initial parameters
        self.refresh = 4
        self.cmode = 0
        self.size = 0

    def control(self, waiting_time, color_mode, size):
        self.refresh = int(round(waiting_time*20))+4
        self.cmode = int(color_mode*1.9)
        self.size = size

    def label(self):
        return ['waiting time', self.refresh,
                'color mode', self.colormodes[self.cmode][0],
                'self.size', self.size]


    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])
        # create smaller world
        tempworld = np.zeros([10, 10, 10])

        # draw (or don't) depending on state
        if self.state == 0:
            # find new point
            self.point = [randint(0, 9), randint(0, 9), randint(0, 9)]
            self.direction = randint(0, 2)

            # draw
            tempworld[self.point[0], self.point[1], self.point[2]] = 1.0

            self.state += 1
        elif self.state == self.refresh or self.state == 20:
            self.state == 0
        elif self.state == 2:
            # draw a 3x3 plane in the chosen plane
            if self.direction == 0:
                tempworld[self.point[0]-1:self.point[0]+2,
                          self.point[1]-1:self.point[1]+2,
                          self.point[2]] = 1.0
            elif self.direction == 1:
                tempworld[self.point[0]-1:self.point[0]+2,
                          self.point[1],
                          self.point[2]-1:self.point[2]+2] = 1.0
            elif self.direction == 2:
                tempworld[self.point[0],
                          self.point[1]-1:self.point[1]+2,
                          self.point[2]-1:self.point[2]+2] = 1.0

            # make central zero again
            tempworld[self.point[0], self.point[1], self.point[2]] = 0.0
        else:
            self.state += 1

        # color mode
        if self.state == 0:
            color = self.colormodes[self.cmode][1]
        elif self.state == 2:
            color = self.colormodes[self.cmode][2]
        else:
            color = [1.0, 1.0, 1.0]

        # path world together
        world[0, :, :, :] = color[0]*tempworld
        world[1, :, :, :] = color[1]*tempworld
        world[2, :, :, :] = color[2]*tempworld

        return np.clip(world, 0, 1)
