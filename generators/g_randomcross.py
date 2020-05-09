# modules
import numpy as np
from random import randint, choice

class g_randomcross():

    def __init__(self):
        self.number = 2
        self.length = 3

    #Strings for GUI
    def return_values(self):
        return [b'randomcross', b'number(1/2/3)', b'length', b'', b'']

    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.number = int(args[0]*2)
        self.length = int(args[1]*10)

        world = np.zeros([3, 10, 10, 10])
        xpos = randint(0,9)
        ypos = randint(0,9)
        zpos = randint(0,9)
        number = [0,1,2]

        xmin = xpos-self.length
        if xmin<0: xmin=0
        xmax = xpos+self.length
        if xmax>9: xmax=9
        ymin = ypos-self.length
        if ymin<0: ymin=0
        ymax = ypos+self.length
        if ymax>9: ymax=9
        zmin = zpos-self.length
        if zmin<0: zmin=0
        zmax = zpos+self.length
        if zmax>9: zmax=9

        for x in range(0, self.number+1):
                direction = choice(number)

                number.remove(direction)

                '''
                if direction == 0:
                    world[:,:,ypos,zpos] = 1
                elif direction == 1:
                    world[:,xpos,:,zpos] = 1
                elif direction == 2:
                    world[:,xpos,ypos,:] = 1
                '''
                if direction == 0:
                    world[:,xmin:xmax+1,ypos,zpos] = 1
                elif direction == 1:
                    world[:,xpos,ymin:ymax+1,zpos] = 1
                elif direction == 2:
                    world[:,xpos,ypos,zmin:zmax+1] = 1

        return np.clip(world, 0, 1)
