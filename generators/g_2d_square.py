# modules
import numpy as np
from random import randint
from convert2d import convert2d

class g_2d_rain():

    def __init__(self):
        self.wait = 10
        self.step = 15

        # first 10 frames outside
        # then inside



    def control(self, waiting frames, blub1, blub2):
        self.wait   =  int(speed*9)

    def label(self):
        return ['Waiting frames', self.wait,'empty', 'empty', 'empty', 'empty']

    def generate(self, step, dumpworld):

        world_2d = np.zeros([3, 20, 40])

        if self.step > 5:
            world[:, :, step] = 1.0
            world[:, :, 39 - step] = 1.0
            world[:, 19-step, :] = 1.0

            self.step -= 1
        elif self.step <= -self.wait:
            self.step = 15
        else:
            self.step -= 1

        world = convert2d(world_2d)

        return np.clip(world, 0, 1)
