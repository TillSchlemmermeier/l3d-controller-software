# modules
import numpy as np
from random import randint
from scipy.signal import fftconvolve, gaussian


class g_columns():
    '''
    Generator:
    '''

    def __init__(self):
        self.reset = 200
        self.blur = 0.1
        self.osc_speed = 0.1
        self.safe_world = np.zeros([10, 10, 10])
        self.y = 2
        self.z = 2
        self.counter = 0

    def control(self, reset, speed, blur):
        self.blur = round(blur*4)
        self.reset = int(reset * 200)
        self.osc_speed = speed*0.1

    def label(self):
        return ['reset', round(self.reset, 2),
                'oscillator speed',  round(self.osc_speed, 2),
                'blur', round(self.blur, 2)]

    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

        if self.counter > self.reset:
            self.y = randint(0, 9)
            self.z = randint(0, 9)
            self.counter = 0

        # shift old world one down
        self.safe_world = np.roll(self.safe_world, shift=1, axis=0)
        self.safe_world[0,:,:] = 0

        # create new spot in the upper most layer and blur it
        world[0, 0, self.y, self.z] = np.sin(step*self.osc_speed)**6
        world[0, :, :, :] = blur(world[0, :,:,:], self.blur*np.sin(step*self.osc_speed)*0.5 + 0.5)

        # copy old world into new world
        world[0, :, :, :] += self.safe_world
        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        # save new world
        self.safe_world = world[0, :, :, :]

        self.counter += 1

        return np.clip(world, 0, 1)

def blur(world, amount = 0.1):
    '''
    Effect: Blur
    '''

    # save previous max value for scaling
    old_max = world.max()

    # create gaussian window
    dim = 5
    a = gaussian(dim, amount+0.001, sym=True)**4
    gauss = np.zeros([dim, dim, dim])
    center = 3

    gauss[center-2:center+3, center-2:center+3, center-2:center+3] = a[0]
    gauss[center-1:center+2, center-1:center+2, center-1:center+2] = a[1]
    gauss[center, center, center] = a[2]

    # convolute with gaussian
    world = fftconvolve(world, gauss, mode='same')

    return np.round(np.clip(world, 0, 1), 2)
