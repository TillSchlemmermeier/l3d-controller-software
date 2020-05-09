# modules
import numpy as np
from random import randint

class e_cut_cube():
    '''
    Effect: e_cut_cube
    '''

    def __init__(self):
        self.speed = 2
        self.step = 0

    #strings for GUI
    def return_values(self):
        return [b'cut_cube', b'speed', b'', b'', b'']

    def control(self, speed, blub0, blub1):
        self.speed = int(speed*10)+1

    def generate(self, step, world):
        num = randint(0,7)

        if self.step % self.speed == 0:

            if num == 0:
                world[:, :5, :5, :5] = 0
            if num == 1:
                world[:, :5, :5, 5:] = 0
            if num == 2:
                world[:, :5, 5:, :5] = 0
            if num == 3:
                world[:, 5:, :5, :5] = 0
            if num == 4:
                world[:, :5, 5:, 5:] = 0
            if num == 5:
                world[:, 5:, :5, 5:] = 0
            if num == 6:
                world[:, 5:, 5:, :5] = 0
            if num == 7:
                world[:, 5:, 5:, 5:] = 0

            self.step += 1

        return np.clip(world, 0, 1)
