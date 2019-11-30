# modules
import numpy as np

class e_squared():

    def __init__(self):
        self.speed = 1

    def control(self, speed, blub0, blub1):
        self.speed = 1.0 + speed

    def label(self):
        return ['exponent', round(self.exponent,2),'empty', 'empty','empty','empty']

    def generate(self, step, world):

        world = world**self.exponent

        return np.clip(world, 0, 1)
