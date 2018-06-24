# modules
import numpy as np


class g_wavepatter():
    '''
    Generator: wavepattern
    '''

    def __init__(self):
        self.freq = 1.0
        self.speed = 1.0

    def control(self, freq, speed, blub1):
        self.freq = freq
        self.speed = speed

    def label(self):
        return ['Frequency', round(self.freq, 2),
                'Speed', self.speed,
                'empty', 'empty']

    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

        for x in range(10):
            for y in range(10):
                for z in range(10):
                    world[:,x,y,z] = np.sin(self.speed * step)*\
                                    (np.sin(0.1*self.freq(x*y*z)))

        return np.clip(world, 0, 1)
