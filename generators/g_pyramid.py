# modules
import numpy as np
from scipy.signal import sawtooth

class g_pyramid():
    '''
    Generator: pyramid

    A pyramid...

    Parameters:
    - size
    - speed
    - orientation: up / down / mirror
    '''

    def __init__(self):
        self.size = 1
        self.speed = 0.2
        self.step = 0
        self.orientation = 1

    #Strings for GUI
    def return_values(self):
        return [b'pyramid', b'size', b'speed', b'orientation', b'']

    def return_gui_values(self):
        if self.orientation < 0.3:
            ori = 'up'
        elif self.orientation > 0.7:
            ori = 'mirror'
        else:
            ori = 'down'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.size,2)), str(round(self.speed,2)), ori, ''),'utf-8')


    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.size = int(args[0]+1.5)
        self.speed = args[1]
        self.orientation = args[2]

        # create world
        world = np.zeros([3, 10, 10, 10])

        if self.orientation < 0.3:
            pyramidup(world, self.size)

        elif self.orientation > 0.7:
            pyramidup(world, self.size)
            pyramiddown(world, self.size)

        else:
            pyramiddown(world, self.size)

        # brightness
        for x in range(10):
            world[:,x,:,:] *= sawtooth(self.speed*self.step+x, width = 1)

        self.step += 1

        return np.clip(world, 0, 1)

def pyramidup(world, size):
    # straight lines
    world[:,0,:,0] = 1.0
    world[:,0,0,:] = 1.0
    world[:,0,:,9] = 1.0
    world[:,0,9,:] = 1.0

    # diagonal random_lines
    for i in range(1,5):
        if size == 2:
            world[:,i*2,i,i] = 1.0
            world[:,i*2,9-i,i] = 1.0
            world[:,i*2,i,9-i] = 1.0
            world[:,i*2,9-i,9-i] = 1.0

            world[:,i*2+1,i,i] = 1.0
            world[:,i*2+1,9-i,i] = 1.0
            world[:,i*2+1,i,9-i] = 1.0
            world[:,i*2+1,9-i,9-i] = 1.0
        else:
            world[:,i,i,i] = 1.0
            world[:,i,9-i,i] = 1.0
            world[:,i,i,9-i] = 1.0
            world[:,i,9-i,9-i] = 1.0

    return(world)


def pyramiddown(world, size):
    # straight lines
    world[:,9,:,0] = 1.0
    world[:,9,0,:] = 1.0
    world[:,9,:,9] = 1.0
    world[:,9,9,:] = 1.0

    # diagonal random_lines
    for i in range(1,5):
        if size == 2:
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

    return(world)
