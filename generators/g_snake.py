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
#        self.world[:, randint(0, 9), randint(0, 9), randint(0, 9)] = 1.0
        self.world[:, 4, 4, 4] = 1.0


    def return_values():
        pass#return {'Number of LEDs', self.number_of_leds}

    def __call__(self, args):
        self.turnprop = args[0]



        world = np.zeros([3,10,10,10])

        # choose direction

        if uniform(0, 1) > self.turnprop:

            oldaxis = self.axis
            while oldaxis == self.axis:
                self.axis = randint(1, 3)

            self.direction = choice([-1, 1])

        world = np.roll(self.world, self.direction, self.axis)
        self.world = world

        return np.clip(world, 0, 1)
