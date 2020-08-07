# modules
import numpy as np
from random import randint, choice

class g_randomcross():

    def __init__(self):
        self.number = 2
        self.length = 3
        self.reset = 1
        self.counter = 0
        self.saveworld = np.zeros([3,10,10,10])

    #Strings for GUI
    def return_values(self):
        return [b'randomcross', b'number', b'length', b'wait', b'']

    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.number = int(args[0]*2)
        self.length = int(args[1]*10)
        self.reset = int(args[2]*10+1)

        world = np.zeros([3, 10, 10, 10])

        if self.counter % self.reset == 0:
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
        else:
            world = self.saveworld


        self.counter +=1
        self.saveworld = world

        return np.clip(world, 0, 1)
