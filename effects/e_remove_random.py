# modules
import numpy as np
from random import randint

class e_remove_random():

    def __init__(self):
        self.n = 1

    def control(self, speed, blub0, blub1):
        self.n = int(speed*100)+1

    def label(self):
        return ['leds to remove',self.n,'empty', 'empty','empty','empty']

    def generate(self, step, world):

        # first, check wether something is on
        if not np.any(world > 0):
            pass
        else:
            # first, sum colors together
            brightness_word = np.sum(world, axis = 0)

            # get list of on leds
            on_list = np.where(world > 0)

            # get number of leds to turn off
            if np.shape(on_list)[0] < self.n:
                self.n = np.shape(on_list)[0]

            for i in range(self.n):
                # get random index
                rand_ind = np.randint(0, np.shape(on_list)[0])

                x = on_list[0, randint]
                y = on_list[1, randint]
                z = on_list[2, randint]

                # turn led off
                world[:, x, y, z] = 0

        return np.clip(world, 0, 1)
