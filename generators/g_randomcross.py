# modules
import numpy as np
from random import randint, choice

class g_randomcross():

    def __init__(self):
        self.number = 2
        self.length = 3

    def control(self, number, length,blub):
        self.number = int(number*2)
        self.length = int(length*10)

    def label(self):
        return ['Number of lines',self.number,'Length', self.length,'empty','empty']

    def generate(self, step, dumpworld):

        world = np.zeros([3, 10, 10, 10])
        xpos = randint(0,9)
        ypos = randint(0,9)
        zpos = randint(0,9)
        number = [0,1,2]

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
                xmin = xpos-self.length
                if xmin<0: xmin=0
                xmax = xpos+self.length
                if xmax>9: xmax=9
                ymin = ypos+self.length
                if ymin<0: ymin=0
                ymax = ypos+self.length
                if ymax>9: xmax=9
                zmin = zpos+self.length
                if zmin<0: zmin=0
                zmax = zpos+self.length
                if zmax>9: zmax=9

                if direction == 0:
                    world[:,xmin:xmax,ypos,zpos] = 1
                elif direction == 1:
                    world[:,xpos,ymin:ymax,zpos] = 1
                elif direction == 2:
                    world[:,xpos,ypos,zmin:zmax] = 1

        return np.clip(world, 0, 1)
