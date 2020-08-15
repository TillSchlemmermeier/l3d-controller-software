# modules
import numpy as np
from random import randint

class g_trees():
    '''
    Generator: cube

    a cube in the cube

    Parameters:
    - size
    - sides y/n : just the edges or also the sides of the cube?
    '''

    def __init__(self):
        self.nled = 1
        self.speed = 2
        self.flatworld = np.zeros([4,10,10])
        self.step = 0
        self.reset = 1

    #Strings for GUI
    def return_values(self):
        return [b'trees', b'N LEDs', b'speed', b'wait', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.nled,2)), str(round(self.speed,2)), str(round(self.reset,2)), ''),'utf-8')

    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.nled = int(round(args[0]*4)+1)
        self.speed = 5-int((args[1]*4))
        self.reset = int(args[2]*5+1)
        world = np.zeros([3,10,10,10])

        if self.step % self.reset == 0:
            for i in range(self.nled):
                self.flatworld[randint(0,3), 9, randint(0,9)] = 1.0


        world[0, :, :, 0] = self.flatworld[0, :, :]
        world[0, :, 9, :] = self.flatworld[1, :, :]
        world[0, :, :, 9] = self.flatworld[2, :, :]
        world[0, :, 0, :] = self.flatworld[3, :, :]

        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        if self.step % self.speed == 0:
            self.flatworld = np.roll(self.flatworld, shift = -1, axis = 1)
            self.flatworld = np.roll(self.flatworld, shift = randint(-1,1), axis = 2)

            self.flatworld[:, 9, :] = 0.0

        self.step += 1
        return np.clip(world, 0, 1)
