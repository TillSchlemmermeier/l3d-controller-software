# modules
import numpy as np


class e_rainbow():
    '''
    Effect: fade2self.blue

    fades the cube to self.blue by moving some of the self.green and self.red
    to the self.blue

    Parameters:
    - amount: how much is moved from the r/g channel to the b channel
    '''

    def __init__(self):
        self.speed = 0.5
        self.red = 1.0
        self.green = 1.0
        self.blue = 0.0

    def control(self, speed, blub0, blub1):
        self.speed = speed

    def label(self):
        return ['speed',round(self.speed),'empty', 'empty','empty','empty']

    def generate(self, step, world):

        if(self.red>0.99 and self.blue<0.99 and self.green<0.01):
            self.blue = self.blue+self.speed
        elif(self.blue>0.99 and self.red>0.01 and self.green<0.01):
            self.red = self.red-self.speed
        elif(self.blue>0.99 and self.green<0.99 and self.red<0.01):
            self.green = self.green+self.speed
        elif(self.green>0.99 and self.blue>0.01 and self.red<0.01):
            self.blue = self.blue-self.speed
        elif(self.green>0.99 and self.red<0.99 and self.blue<0.01):
            self.red = self.red+self.speed
        elif(self.red>0.99 and self.green>0.01 and self.blue<0.01):
            self.green = self.green-self.speed

        self.red, self.blue, self.green = np.clip([self.red,self.blue,self.green],0,1)

        world[0, :, :, :] = world[0, :, :, :]*self.red
        world[1, :, :, :] = world[1, :, :, :]*self.green
        world[2, :, :, :] = world[2, :, :, :]*self.blue



        return np.clip(world, 0, 1)

'''
def generateRainbowWorld(world, self.red, self.green, self.blue, self.speed):
    new_world_r = world_init(10)
    new_world_g = world_init(10)
    new_world_b = world_init(10)

    if(self.red>0.99 and self.blue<0.99 and self.green<0.01):
        self.blue = self.blue+self.speed
    elif(self.blue>0.99 and self.red>0.01 and self.green<0.01):
        self.red = self.red-self.speed
    elif(self.blue>0.99 and self.green<0.99 and self.red<0.01):
        self.green = self.green+self.speed
    elif(self.green>0.99 and self.blue>0.01 and self.red<0.01):
        self.blue = self.blue-self.speed
    elif(self.green>0.99 and self.red<0.99 and self.blue<0.01):
        self.red = self.red+self.speed
    elif(self.red>0.99 and self.green>0.01 and self.blue<0.01):
        self.green = self.green-self.speed

    self.red, self.blue, self.green = np.clip([self.red,self.blue,self.green],0,1)

    for x in range(len(world)):
        for y in range(len(world)):
            for z in range(len(world)):
                if(world[x,y,z]!=0):
                    new_world_b[x,y,z]=self.blue
                    new_world_r[x,y,z]=self.red
                    new_world_g[x,y,z]=self.green

    return {'r':new_world_r, 'g':new_world_g, 'b':new_world_b, 'rW':self.red,'gW':self.green,'bW':self.blue,}
'''
