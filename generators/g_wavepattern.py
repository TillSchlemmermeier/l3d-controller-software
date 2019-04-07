# modules
import numpy as np


class g_wavepattern():
    '''
    Generator: wavepattern
    '''

    def __init__(self):
        self.freq = 0.5
        self.speed = 1.0

    def return_values(self):
        pass

    #def control(self, freq, speed, blub1):
    def __call__(self, args):
        self.freq = int(args[0]*10)
        self.speed = args[1]*0.5



    #def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

        for x in range(10):
            for y in range(10):
                for z in range(10):
                    world[:, x, y, z] = np.sin(step*self.speed)*(
                                        np.sin(np.pi*self.freq*x/10)**6+\
                                        np.sin(np.pi*self.freq*y/10)**6+\
                                        np.sin(np.pi*self.freq*z/10)**6)

        return np.clip(world, 0, 1)
