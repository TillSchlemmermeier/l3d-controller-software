# modules
import numpy as np
from generators.g_orbiter import g_orbiter

class a_orbbot():
    '''
    Generator: Testbot
    '''

    def __init__(self):
        self.counter = 1

    #Strings for GUI
    def return_values(self):
        return [b'a_orbbot', b'', b'', b'', b'']

    def __call__(self, args):
        pass

        # create world
        world = np.zeros([3, 10, 10, 10])

        generator = g_orbiter()

        generator.control(0.5*(np.sin(self.counter * 0.01)*0.5+0.5),0.4,0.05)

        world[:, :, :, :] = generator.generate(self.counter, 0)

        self.counter += 1

        return np.clip(world, 0, 1)
