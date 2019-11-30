# modules
import numpy as np
from random import randint
from generators.convert2d import convert2d
from scipy.signal import convolve2d

class g_2d_conway():

    def __init__(self, test = False, dim = [60, 10]):
        self.number = 100
        self.dim = dim
        self.test = test
        self.state = 'populate' # evolve, wait
        self.lastworld = np.zeros([3, dim[0], dim[1]])
        self.counter = 0
        self.steps = 20
        self.wait = 4

    def control(self, *args):
        self.number = int(args[0]*100)+1
        self.steps  = int(args[1]*50)+10
        self.wait   = int(args[2] * 20)

    def label(self):
        return ['Number',self.number,'Steps', self.steps,'Waiting frames',self.wait]

    def generate(self, step, dumpworld):

        world_2d = np.zeros([3, self.dim[0], self.dim[1]])

        if self.state == 'populate':
            for i in range(self.number):
                world_2d[:, randint(0,self.dim[0]-1), randint(0,self.dim[1]-1)] = 1.0

            # test blinker
            # world_2d[:, 10, 5:7] = 1.0
            # world_2d[:, 9:12, 6] = 1.0


            self.state = 'evolve'
            self.counter = self.steps

        elif self.state == 'evolve':

            world_2d[0, :, :] = life(self.lastworld[0, :, :])
            world_2d[1, :, :] = world_2d[0, :, :]
            world_2d[2, :, :] = world_2d[0, :, :]

            if self.counter < 0:
                self.state = 'wait'
                self.counter = self.wait
            else:   
                self.counter -= 1

        elif self.state == 'wait':
            if self.counter < 0:
                self.state = 'populate'
            else:
                self.counter -= 1


        self.lastworld = world_2d

        if not self.test:
            # convert it to 2d
            world = convert2d(world_2d)
        else:
            world = world_2d

        return np.clip(world, 0, 1)



def life(X):
    """
     Conway's Game of Life.
     - X, matrix with the initial state of the game.
     - steps, number of generations.
    """

    def roll_it(x, y):
        # r
        # x=1, y=0 on the left;  x=-1, y=0 right;
        # x=0, y=1 top; x=0, y=-1 down; x=1, y=1 top left; ...
        return np.roll(np.roll(X, y, axis=0), x, axis=1)


#    for _ in range(steps):
        # count the number of neighbours 
        # the universe is considered toroidal
    Y = roll_it(1, 0) + roll_it(0, 1) + roll_it(-1, 0) \
        + roll_it(0, -1) + roll_it(1, 1) + roll_it(-1, -1) \
        + roll_it(1, -1) + roll_it(-1, 1)

    # game of life rules
    X = np.logical_or(np.logical_and(X, Y ==2), Y==3)
    X = X.astype(int)
    return X