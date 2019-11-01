# modules
import numpy as np
from random import randint
from convert2d import convert2d

class g_2d_rain():

    def __init__(self):
        self.number =  1
        self.wait   =  1
        self.dir    = -1

    def control(self, number, speed, direction):
        self.number = number
        self.wait   = 10 - int(speed*9)

        if direction > 0.5:
            self.dir = -1
        else:
            self.dir =  1

    def label(self):
        return ['Number',self.number,'Speed', self.wait,'Up/Down',self.dir]

    def generate(self, step, dumpworld):

        world_2d = np.zeros([3, 20, 40])

        # turn on led
        if step % self.wait == 0:
            for i in self.number:
                if self.dir == -1
                    world_2d[:, 9, randint(0,39)] = 1.0
                else
                    world_2d[:, 0, randint(0,39)] = 1.0
        # roll
        world_2d = np.roll(world_2, axis = 1, shift = self.dir)

        # convert it to 2d
        world = convert2d(world_2d)

        return np.clip(world, 0, 1)
