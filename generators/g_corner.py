
import numpy as np

class g_corner():
    '''
    Generator: corner
    '''

    def __init__(self):
        self.size = 0

    #Strings for GUI
    def return_values(self):
        return [b'corner', b'size', b'', b'', b'']

    def __call__(self, args):
        self.size = int(args[0]*5)

        # create world
        world = np.zeros([3, 10, 10, 10])

        # switch on corners
        world[:,0:self.size,0:self.size,0:self.size] = 1.0
        world[:,0:self.size,0:self.size,10-self.size:] = 1.0
        world[:,0:self.size,10-self.size:,0:self.size] = 1.0
        world[:,10-self.size:,0:self.size,0:self.size] = 1.0
        world[:,0:self.size,10-self.size:,10-self.size:] = 1.0
        world[:,10-self.size:,0:self.size,10-self.size:] = 1.0
        world[:,10-self.size:,10-self.size:,0:self.size] = 1.0
        world[:,10-self.size:,10-self.size:,10-self.size:] = 1.0

        return np.clip(world, 0, 1)
