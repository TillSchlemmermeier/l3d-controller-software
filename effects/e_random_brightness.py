# modules
import numpy as np
from random import uniform

class e_random_brightness():

    def __init__(self):
        self.speed = 1
        self.brightness = uniform(0,1)

    def control(self, speed, blub0, blub1):
        self.speed = int(speed*10)

    def label(self):
        return ['speed', self.speed,'empty', 'empty','empty','empty']

    def generate(self, step, world):

        if step % self.speed == 0.0:
            self.brighness = uniform(0, 1)

        return np.clip(world*self.brightness, 0, 1)
