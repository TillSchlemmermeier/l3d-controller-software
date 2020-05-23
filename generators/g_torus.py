# modules
import numpy as np

class g_torus():
    '''
    Generator: torus

    creates a torus

    Parameters:
    - radius
    - thickness
    '''

    def __init__(self):
        self.radius = 6
        self.thickness = 3


    #Strings for GUI
    def return_values(self):
        return [b'torus', b'radius', b'thickness', b'', b'']

    #def control(self, maxsize, growspeed, oscillate):
    def __call__(self, args):
        self.radius     = args[0]*10
        self.thickness  = args[1]*5

        #def generate(self, step, dumpworld):
        world = np.zeros([3, 10, 10, 10])

        # create torus
        world[:,:,:,:] = 1.0

        return np.round(np.clip(world, 0, 1), 3)
