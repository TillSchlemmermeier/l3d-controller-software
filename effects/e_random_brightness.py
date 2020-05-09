# modules
import numpy as np
from random import uniform

class e_random_brightness():

    def __init__(self):
        self.speed = 1
        self.brightness = uniform(0,1)
        self.step = 0

    #strings for GUI
    def return_values(self):
        return [b'random_brightness', b'speed', b'', b'', b'']

    def control(self, speed, blub0, blub1):
        self.speed = int(speed*10)+1

    def generate(self, step, world):

        if self.step % self.speed == 0:
            self.brightness = uniform(0, 1)

        self.step += 1

        return np.clip(world*self.brightness, 0, 1)
