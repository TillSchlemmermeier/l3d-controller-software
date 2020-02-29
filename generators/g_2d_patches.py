# modules
import numpy as np
from random import randint
from generators.convert2d import convert2d

class g_2d_patches():

    def __init__(self, test = False, dim = [20, 10]):
        self.pos = [randint(0,54), randint(1,4)]
        self.dim = dim
        self.test = test

        # make empty patches
        self.patch_frames = []
        for i in range(5):
            self.patch_frames.append(np.zeros([6,5]))

        # fill patches
        self.patch_frames[0][1:5, 2] = 0.2
        self.patch_frames[0][2:4, 1:4] = 0.2

        self.patch_frames[1][1:5, 2] = 0.5
        self.patch_frames[1][2:4, 1:4] = 0.5

        self.patch_frames[2][1:5, 1:4] = 0.3
        self.patch_frames[2][2:4, :] = 0.3
        self.patch_frames[2][:, 2] = 0.3
        self.patch_frames[2][1:5, 2] = 0.5
        self.patch_frames[2][2:4, 1:4] = 0.5

        self.patch_frames[3][1:5, 1:4] = 1.0
        self.patch_frames[3][2:4, :] = 1.0
        self.patch_frames[3][:, 2] = 1.0
        self.patch_frames[3][1:5, 2] = 0.2
        self.patch_frames[3][2:4, 1:4] = 0.2

        self.patch_frames[4][1:5, 1:4] = 5.0
        self.patch_frames[4][2:4, :] = 5.0
        self.patch_frames[4][:, 2] = 5.0
        self.patch_frames[4][1:5, 2] = 0.0
        self.patch_frames[4][2:4, 1:4] = 0.0


        self.counter = len(self.patch_frames)


    def control(self, number, speed, direction):
        pass

    def label(self):
        return ['empty','empty','empty', 'empty','empty','empty']

    def generate(self, step, dumpworld):

        world_2d = np.zeros([3, self.dim[0], self.dim[1]])

        if self.counter == 0:
            self.counter = len(self.patch_frames)
            self.pos = [randint(0,54), randint(0,4)]

        else:
            world_2d[0, self.pos[0]:self.pos[0]+6, self.pos[1]:self.pos[1]+5] = self.patch_frames[-self.counter]

            world_2d[1, :, :] = world_2d[0, :, :]
            world_2d[2, :, :] = world_2d[0, :, :]

            self.counter -= 1

        if not self.test:
            # convert it to 2d
            world = convert2d(world_2d)
        else:
            world = world_2d

        return np.clip(world, 0, 1)
