# modules
import numpy as np
from scipy.signal import sawtooth

class g_pyramid_upsidedown():
    '''
    Generator: pyramid
    '''

    def __init__(self):
        self.size = 1
        self.speed = 0.2
        self.step = 0

    #Strings for GUI
    def return_values(self):
        return [b'pyramid_upsidedown', b'size', b'speed', b'', b'']

    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.size = int(args[0]+1.5)
        self.speed = args[1]

        # create world
        world = np.zeros([3, 10, 10, 10])

        # straight lines
        world[:,9,:,0] = 1.0
        world[:,9,0,:] = 1.0
        world[:,9,:,9] = 1.0
        world[:,9,9,:] = 1.0

        # diagonal random_lines
        for i in range(1,5):
            if self.size == 2:
                world[:,9-i*2,i,i] = 1.0
                world[:,9-i*2,9-i,i] = 1.0
                world[:,9-i*2,i,9-i] = 1.0
                world[:,9-i*2,9-i,9-i] = 1.0

                world[:,9-i*2,i,i] = 1.0
                world[:,9-i*2,9-i,i] = 1.0
                world[:,9-i*2,i,9-i] = 1.0
                world[:,9-i*2,9-i,9-i] = 1.0
            else:
                world[:,9-i,i,i] = 1.0
                world[:,9-i,9-i,i] = 1.0
                world[:,9-i,i,9-i] = 1.0
                world[:,9-i,9-i,9-i] = 1.0

        # brightness
        for x in range(10):
            world[:,x,:,:] *= sawtooth(self.speed*self.step+x, width = 0)

        self.step += 1

        return np.clip(world, 0, 1)
