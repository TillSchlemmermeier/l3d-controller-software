# modules
import numpy as np
from scipy.signal import fftconvolve, gaussian

class e_blur():
    '''
    Effect: e_blur
    '''

    def __init__(self):
        self.blur = 0.1

    #strings for GUI
    def return_values(self):
        return [b'blur', b'blur intensity', b'', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(self.blur), '', '', ''), 'utf-8')

    def __call__(self, world, args):
        # parsing input
        self.blur = round(args[0],3)

        # create gaussian window
        dim = 5
        a = gaussian(dim, self.blur+0.001, sym=True)**2
        gauss = np.zeros([dim, dim, dim])
        center = 3

#        gauss[center-3:center+4, center-3:center+4, center-3:center+4] = a[0]
        gauss[center-2:center+3, center-2:center+3, center-2:center+3] = a[1]
        gauss[center-1:center+2, center-1:center+2, center-1:center+2] = a[2]
        gauss[center, center, center] = a[3]

        # convolute with gaussian
        world[0, :, :, :] = fftconvolve(world[0, :, :, :], gauss, mode='same')
        world[1, :, :, :] = fftconvolve(world[1, :, :, :], gauss, mode='same')
        world[2, :, :, :] = fftconvolve(world[2, :, :, :], gauss, mode='same')

        return np.clip(world, 0, 1)
