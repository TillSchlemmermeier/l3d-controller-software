import numpy as np
from random import randint, uniform, choice


class g_snake():
    '''
    Generator: snake

    A snake!

    Parameters:
    - number   : Number of snakes running around
    - turnprop : propability of doing a turn
    '''

    def __init__(self):
        self.number = 1
        self.turnprop = 0.25

        # create an internal world with i snake point
        self.axis = 0
        self.direction = 1

        self.world = np.zeros([3, 10, 10, 10])
        self.world[:, randint(0, 9), randint(0, 9), randint(0, 9)] = 1.0

    def control(self, number, turnprop, blub1):
        self.turnprop = turnprop

    def generate(self, step):

        # choose direction
        if uniform(0, 1) > self.turnprop:
            oldaxis = self.axis
            while oldaxis == self.axis:
                self.axis = randint(1, 3)

            self.direction = choice([-1, 1])

        self.world = np.roll(self.world, self.direction, self.axis)

        return self.world
