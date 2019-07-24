# modules
import numpy as np
from scipy.ndimage.interpolation import rotate

class g_rotating_cube():
    '''
    Generator: cube

    a cube in the cube

    Parameters:
    - size
    - sides y/n : just the edges or also the sides of the cube?
    '''

    def __init__(self):
        self.size = 3
        self.sides = False
        self.xspeed = 0.1
        self.yspeed = 0.1
        self.zspeed = 0.0

    def control(self, xspeed, yspeed, zspeed):
        #self.size = round(size*4)
        self.xspeed = 10*xspeed
        self.yspeed = 10*yspeed
        self.zspeed = 10*zspeed

    def label(self):
        return ['x speed',round(self.xspeed, 2),'y speed', np.round(self.xspeed, 2),'z speed', np.round(self.yspeed, 2)]


    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])
        # create smaller world
        tempworld = np.zeros([10, 10, 10])

        tempworld[:, :, :] = -1.0

        size = self.size

        # write cube
        # x slices
        tempworld[4-size, 4-size:6+size, 4-size:6+size] += 1
        tempworld[5+size, 4-size:6+size, 4-size:6+size] += 1
        # y slices
        tempworld[4-size:6+size, 4-size, 4-size:6+size] += 1
        tempworld[4-size:6+size, 5+size, 4-size:6+size] += 1
        # z slices
        tempworld[4-size:6+size, 4-size:6+size, 4-size] += 1
        tempworld[4-size:6+size, 4-size:6+size, 5+size] += 1

        # rotate
        newworld = rotate(tempworld, step*self.xspeed,
                          axes = (1,2), order = 1,
	                      mode = 'nearest', reshape = False)

        newworld = rotate(newworld, step*self.yspeed,
                          axes = (0,1), order = 1,
	                      mode = 'nearest', reshape = False)

        newworld = rotate(newworld, step*self.zspeed,
                          axes = (0,2), order = 1,
	                      mode = 'nearest', reshape = False)

        # path world together
        world[0, :, :, :] = newworld
        world[1, :, :, :] = newworld
        world[2, :, :, :] = newworld

        return np.clip(world, 0, 1)
