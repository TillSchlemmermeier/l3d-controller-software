# modules
import numpy as np

class e_staticcolor():
    '''
    Effect: static color



    Parameters:
    - red
    - green
    - blue
    '''

    def __init__(self):
        self.red = 1.0
        self.green = 1.0
        self.blue = 1.0

    def control(self, red, green, blue):
        self.red = round(red,2)
        self.green = round(green,2)
        self.blue = round(blue,2)

    def label(self):
        return ['RED',self.red,'GREEN', self.green,'BLUE',self.blue]

    def generate(self, step, world):

        world[0, :, :, :] = world[0, :, :, :]*self.red
        world[1, :, :, :] = world[1, :, :, :]*self.green
        world[2, :, :, :] = world[2, :, :, :]*self.blue

        return np.clip(world, 0, 1)
