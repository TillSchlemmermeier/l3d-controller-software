# modules
import numpy as np
from random import randint, choice

class g_random_grow():

    def __init__(self):
        self.world = np.zeros([10, 10, 10])
        self.number = 2
        self.speed = 0.1

    def return_state(self):
        return [
            ['number', 'number', round(self.number,2)],
            ['speed', 'speed', round(self.speed,2)],
        ]

    def __call__(self, args):
        # === PARAMETERS START ===
        self.number = int(args[0]*20)+1
        self.speed = args[1]*0.1
        # === PARAMETERS END ===

        for i in range(self.number):
            self.world[randint(0,9), randint(0,9), randint(0,9)] += choice([-0.2, 0.2])

        # clip
        self.world = np.clip(self.world, 0, 1)

        # increase
        self.world *= 1+self.speed

        # delete if necessary
        self.world[np.where(self.world > 0.98)] = 0

        # create final world
        world = np.zeros([3, 10, 10, 10])
        for i in range(3):
            world[i, :, :, :] = self.world**4

        return np.clip(world, 0, 1)
