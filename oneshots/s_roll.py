import numpy as np
from random import choice

class s_roll:

    def __init__(self):
        self.counter = 4
        self.direction = choice([-1, 1])
        self.axis = choice([1,2,3])

    def __call__(self, world):

        if self.counter > 0:
            world = np.roll(world, shift = int(self.direction*(5-self.counter)), axis = self.axis)
            self.counter -= 1

        return world, self.counter
