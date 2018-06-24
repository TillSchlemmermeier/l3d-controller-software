# modules
import numpy as np


class g_cube():
    '''
    Generator: cube

    a cube in the cube

    Parameters:
    - size
    - sides y/n : just the edges or also the sides of the cube?
    '''

    def __init__(self):
        self.numbers = 1
        self.fade = 0.5
        self.lastworld = np.zeros([10, 10, 10])

    def control(self, numbers, fade, blub1):
        self.numbers = int(numbers*10 + 1)
        self.fade = fade

    def label(self):
        return ['Numbers', numbers,
                'fade', self.fade,
                'empty', 'empty']

    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

        # move last world 1 step down
        self.lastworld = np.roll(self.lastworld, axis = 0)
        self.lastworld[0, :, :, :] = 0.0

        # turn on random leds in upper level
        for i in range(self.numbers):
            world[0,0,randint(0, 9),randint(0, 9)] = 1.0

        # add last frame
        world[0,:,:,:] += self.lastworld*self.fade
        self.lastworld[:,:,:] = world[0,:,:,:]

        # copy to other colors
        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        return np.clip(world, 0, 1)
