# modules
import numpy as np
from random import uniform

class e_random_brightness():

    def __init__(self):
        self.speed = 1
        self.brightness = uniform(0,1)
        self.step = 0

    def return_state(self):
        return [
            ['speed', 'speed', round(self.speed,1)],
        ]

    def __call__(self, world, args):
        # parsing input
        self.speed = int(args[0]*10)+1

        if self.step % self.speed == 0:
            self.brightness = uniform(0, 1)

        self.step += 1

        return np.clip(world*self.brightness, 0, 1)
