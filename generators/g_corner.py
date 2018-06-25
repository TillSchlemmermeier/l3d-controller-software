
import numpy as np

class g_corner():
    '''
    Generator: corner
    '''

    def __init__(self):
        self.size = 0

    def control(self, size, blub1, blub2):
        self.size = int(size*5)

    def label(self):
        return ['size',round(self.size,2),'empty','empty','empty','empty','empty']

    def generate(self, step, dumpworld):
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
