# modules
import numpy as np
from random import randint
from generators.convert2d import convert2d

class g_2d_square():

    def __init__(self):
        self.wait = 10
        self.step = 0
        self.state = 1

    def control(self, speed, blub1, blub2):
        self.wait   =  int(speed*9)

    def label(self):
        return ['Waiting frames', self.wait,'empty', 'empty', 'empty', 'empty']

    def generate(self, step, dumpworld):

        world_2d = np.zeros([3, 20, 40])

        if self.step < 10:
            world_2d[:, :, self.step] = 1.0
            world_2d[:, :, 39-self.step] = 1.0
            world_2d[:, 19-self.step, :] = 1.0

            self.step += 1
        elif self.step > self.wait+10:
            self.step = 0
        else:
            self.step += 1

        world = convert2d(world_2d)

        return np.clip(world, 0, 1)
