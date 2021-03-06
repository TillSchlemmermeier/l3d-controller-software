# modules
import numpy as np
from random import randint

class e_remove_random():

    def __init__(self):
        self.n = 1

    def control(self, speed, blub0, blub1):
        self.n = int(speed*200)+1

    def label(self):
        return ['leds to remove',self.n,'empty', 'empty','empty','empty']

    def generate(self, step, world):

        for i in range(self.n):
            world[:, randint(0,9), randint(0,9), randint(0,9)] = 0.0

        return np.clip(world, 0, 1)
