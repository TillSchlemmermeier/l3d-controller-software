# modules
import numpy as np
from random import randint
from generators.convert2d import convert2d

class g_2d_square():

    def __init__(self, test = False, dim = [20, 10] ):
        self.wait = 2
        self.step = 0
        self.state = 1
        self.dim = dim
        self.test = test

    def control(self, speed, blub1, blub2):
        self.wait = int(speed*9)

    def label(self):
        return ['Waiting frames', self.wait,'empty', 'empty', 'empty', 'empty']

    def generate(self, step, dumpworld):

        # create world
        world_2d = np.zeros([3, self.dim[0], self.dim[1]])

        # make square bigger
        if self.step < min(self.dim)/2:
            fac = int(max(self.dim) / min(self.dim))
            # print square
            world_2d[:, self.step*fac:self.dim[0]-self.step*fac, self.step:self.dim[1]-self.step] = 1.0

            # make inner white
            world_2d[:, self.step*fac+1:self.dim[0]-self.step*fac-1, self.step+1:self.dim[1]-self.step-1] = 0.0


            self.step += 1
        # waiting frames
        elif self.step > self.wait+min(self.dim)/2:
            self.step = 0
        # reset
        else:
            self.step += 1

        if not self.test:
            # convert it to 2d
            world = convert2d(world_2d)
        else:
            world = world_2d

        return np.clip(world, 0, 1)
