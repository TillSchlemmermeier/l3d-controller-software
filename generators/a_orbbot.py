# modules
import numpy as np
from generators.g_orbiter import g_orbiter

class a_orbbot():
    '''
    Generator: Testbot
    '''

    def __init__(self):
        self.counter = 1
        self.generator = g_orbiter()

    #Strings for GUI
    def return_values(self):
        return [b'a_orbbot', b'', b'', b'', b'']

    def __call__(self, args):

        # create world
        world = np.zeros([3, 10, 10, 10])


        world[:, :, :, :] = self.generator([0.5*(np.sin(self.counter * 0.01)*0.5+0.5), 0.65, 0.05, 0])

        self.counter += 1

        return np.clip(world, 0, 1)
