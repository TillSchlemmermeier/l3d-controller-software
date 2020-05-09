# modules
import numpy as np

class e_squared():

    def __init__(self):
        self.exponent = 1

    #strings for GUI
    def return_values(self):
        return [b'squared', b'exponent', b'', b'', b'']

    def control(self, speed, blub0, blub1):
        self.exponent = 0.5 + speed*2


    def generate(self, step, world):

        world = world**self.exponent

        return np.clip(world, 0, 1)
