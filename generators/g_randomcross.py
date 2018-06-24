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
        return ['empty','empty','empty', 'empty','empty','empty']

    def generate(self, step, dumpworld):

        world = np.zeros([3, 10, 10, 10])
        xpos = randint(0,9)
        ypos = randint(0,9)
        zpos = randint(0,9)
        number = [0,1,2]

        for x in range(0, self.number+1):
                direction = choice(number)
                number.remove(direction)

                
                if direction == 0:
                    world[:,:,ypos,zpos] = 1
                elif direction == 1:
                    world[:,xpos,:,zpos] = 1
                elif direction == 2:
                    world[:,xpos,ypos,:] = 1


                '''
                if direction == 0:
                    world[xpos-self.length:xpos+self.length,ypos,zpos] = 1
                elif direction == 1:
                    world[xpos,ypos-self.length:ypos+self.length,zpos] = 1
                elif direction == 2:
                    world[xpos,ypos,zpos-self.length:zpos+self.length] = 1
                '''

        return np.clip(world, 0, 1)
