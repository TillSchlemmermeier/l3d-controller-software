# modules
import numpy as np


class e_blur():
    '''
    Effect: blur
    '''

    def __init__(self):
        self.amount = 0.1

    def control(self, amount, blub1, blub2):
        self.amount = amount*0.01

    def label(self):
        return ['Blur Amount', round(self.amount*10, 2),
                'empty', 'empty',
                'empty', 'empty']


    def generate(self, step, world):

        world[0,:,:,:] = blur(world[0,:,:,:], self.amount)
        world[1,:,:,:] = blur(world[1,:,:,:], self.amount)
        world[2,:,:,:] = blur(world[2,:,:,:], self.amount)

        return np.clip(world, 0, 1)


def blur(world, amount = 0.1):
    '''
    Effect: Blur
    '''

    # save previous max value for scaling
    # old_max = world.max()

    # create gaussian window
    dim = 7
    a = gaussian(dim, amount+0.001, sym=True)
    gauss = world_init(dim)
    center = 4

    gauss[center-2:center+3, center-2:center+3, center-2:center+3] = a[0]
    gauss[center-1:center+2, center-1:center+2, center-1:center+2] = a[1]
    gauss[center, center, center] = a[2]

    # convolute with gaussian
    world = fftconvolve(world, gauss, mode='same')

    return np.round(np.clip(world, 0, 1), 2)
