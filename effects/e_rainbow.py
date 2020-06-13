# modules
import numpy as np


class e_rainbow:
    '''
    Effect: Rainbow
    '''
    def __init__(self):
        self.speed = 0.5
        self.red = 1.0
        self.green = 1.0
        self.blue = 0.0

    #strings for GUI
    def return_values(self):
        return [b'rainbow', b'speed', b'', b'', b'']

    def __call__(self, world, args):
        # parsing input
        self.speed = args[0]*0.6

        # calculate color
        if self.red>0.99 and self.blue<0.99 and self.green<0.01:
            self.blue = self.blue+self.speed
        elif self.blue>0.99 and self.red>0.01 and self.green<0.01:
            self.red = self.red-self.speed
        elif self.blue>0.99 and self.green<0.99 and self.red<0.01:
            self.green = self.green+self.speed
        elif self.green>0.99 and self.blue>0.01 and self.red<0.01:
            self.blue = self.blue-self.speed
        elif self.green>0.99 and self.red<0.99 and self.blue<0.01:
            self.red = self.red+self.speed
        elif self.red>0.99 and self.green>0.01 and self.blue<0.01:
            self.green = self.green-self.speed

        self.red, self.blue, self.green = np.clip([self.red,self.blue,self.green],0,1)

        world[0, :, :, :] = world[0, :, :, :]*self.red
        world[1, :, :, :] = world[1, :, :, :]*self.green
        world[2, :, :, :] = world[2, :, :, :]*self.blue

        return np.clip(world, 0, 1)
