# modules
import numpy as np


class e_redyellow():
    '''
    Effect: redyellow

    '''

    def __init__(self):
        self.speed = 0.5
        self.red = 1.0
        self.green = 1.0
        self.blue = 0.0

    def control(self, speed, blub0, blub1):
        self.speed = speed*0.1

    def label(self):
        return ['speed',round(self.speed,2),'empty', 'empty','empty','empty']

    def generate(self, step, world):

        self.green = np.sin(self.speed*step)

        world[0, :, :, :] = world[0, :, :, :]*self.red
        world[1, :, :, :] = world[1, :, :, :]*self.green
        world[2, :, :, :] = world[2, :, :, :]*self.blue

        return np.clip(world, 0, 1)
