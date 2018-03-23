# modules
import numpy as np
from random import randint

class g_random():

    def __init__(self):
       self.number = 1

    def control(number, blub0, blub1):
        self.number = (number*10)+1

    def generate(self, step):
        world = np.zeros([3,10,10,10])

        color = randint(0, 2)

        for i in range(self.number):
            world[color, randint(0,9), randint(0, 9), randint(0, 9)] = 1.0
        return world
