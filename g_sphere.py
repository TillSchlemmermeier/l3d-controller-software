# modules
import numpy as np
from random import randint
from joblib import Parallel, delayed
import multiprocessing

class g_sphere():
    '''
    Generator: sphere

    sphere at a random position

    Parameters:
    - size
    '''
    
    def __init__(self):
        self.size = 2
        self.color = 0

    def control(self, color, size, blub0):
        self.size = round(size*10)

    def label(self):
        return ['size',round(self.size,2),'empty', 'empty','empty','empty']

    def generate(self, step, dumpworld):

        world = np.zeros([3, 10, 10, 10])

        posx = randint(0,9)
        posy = randint(0,9)
        posz = randint(0,9)

# map function instead of loop
# numba for performance boost
        for x in range(10):
            for y in range(10):
                for z in range(10):
                    dist = np.sqrt((x-posx)**2+(y-posy)**2+(z-posz)**2)
                    if dist <= self.size:
                        world[:, x, y, z] = 1.0
	
        return np.clip(world, 0, 1)
