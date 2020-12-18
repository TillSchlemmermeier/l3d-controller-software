# modules
import numpy as np
from random import randint
from multiprocessing import shared_memory

class g_darts():
    '''
    Generator:
    '''

    def __init__(self):
        self.safe_world = np.zeros([10, 10, 10])
        self.counter = 0
        self.step = 0
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0

    #Strings for GUI
    def return_values(self):
        return [b'columns', b'number', b'', b'', b'channel']

    def return_gui_values(self):
        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.number,2)), '', '', channel),'utf-8')


    def __call__(self, args):
        self.number = round(args[0]*10)
        self.channel = int(args[3]*4)-1

        # create world
        world = np.zeros([3, 10, 10, 10])

        if self.counter > self.reset:
            self.y = randint(0, 9)
            self.z = randint(0, 9)
            self.counter = 0

        # shift old world one down
        self.safe_world = np.roll(self.safe_world, shift=1, axis=0)
        self.safe_world[0,:,:] = 0


        # check if S2L is activated
        if self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            self.blur = 4 * np.clip(current_volume, 0, 1)

        # create new spot in the upper most layer and blur it
        world[0, 0, self.y, self.z] = np.sin(self.step*self.osc_speed)**6
        world[0, :, :, :] = blur(world[0, :,:,:], self.blur*np.sin(self.step*self.osc_speed)*0.5 + 0.5)

        # copy old world into new world
        world[0, :, :, :] += self.safe_world
        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        # save new world
        self.safe_world = world[0, :, :, :]

        self.counter += 1
        self.step += 1

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
