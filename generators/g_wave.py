# modules
import numpy as np
from random import randint
from scipy.stats import multivariate_normal

class g_wave():

    def __init__(self):
        self.sigma = 1
        self.speed = 1
        self.counter = 0
        self.direction = 0
        self.position = 1
        self.maxsize = 30

    def control(self, sigma, speed, blub1):
        self.sigma = sigma*1.4+0.2
        self.speed = speed*2.5+0.4

    def label(self):
        return ['sigma',round(self.sigma,2),'speed',round(self.speed,2),'empty','empty','empty']

    def generate(self, step, dumpworld):

        world = np.zeros([3, 10, 10, 10])


        a = np.zeros([10,10])

        if self.counter > self.maxsize:
            self.direction = randint(1,8)
            self.position = randint(0,9)
            self.counter = 0

            if self.direction < 5:
                self.maxsize=20
            else:
                self.maxsize=31


        i = self.counter
        direction = self.direction
        position = self.position

        if direction == 1: #x+
            for x in range(10):
    #            a[x,:] = ((np.sin((i)/np.pi + x/np.pi)+1)/2)**4
                a[x,:] = np.exp(-(((x+5-i)/self.sigma)**2)/10)
            self.counter -= 0.3
            world[0,position,:,:] = a
        elif direction == 2: #x-
            for x in range(10):
                a[x,:] = np.exp(-(((x-15+i)/self.sigma)**2)/10)
            self.counter -= 0.3
            world[0,position,:,:] = a
        elif direction == 3: #y+
            for y in range(10):
                a[:,y] = np.exp(-(((y+5-i)/self.sigma)**2)/10)
            self.counter -= 0.3
            world[0,position,:,:] = a
        elif direction == 4: #y-
            for y in range(10):
                a[:,y] = np.exp(-(((y-15+i)/self.sigma)**2)/10)
            self.counter -= 0.3
            world[0,position,:,:] = a
        elif direction == 5: #xy
            for x in range(10):
                for y in range(10):
                    a[x,y] = np.exp(-(((x+y-25+i)/self.sigma)**2)/10) # done
            world[0,position,:,:] = a
        elif direction == 6: #x-y
            for x in range(10):
                for y in range(10):
                    a[x,y] = np.exp(-(((x-y+15-i)/self.sigma)**2)/10) # done
            world[0,position,:,:] = a
        elif direction == 7: #-xy
            for x in range(10):
                for y in range(10):
                    a[x,y] = np.exp(-(((-x+y+15-i)/self.sigma)**2)/10)
            world[0,position,:,:] = a
        elif direction == 8: #-x-y
            for x in range(10):
                for y in range(10):
                    a[x,y] = np.exp(-(((-x-y+25-i)/self.sigma)**2)/10)
            world[0,position,:,:] = a

        world[1,:,:,:]=world[0,:,:,:]
        world[2,:,:,:]=world[0,:,:,:]
        self.counter += 1*self.speed
        return np.clip(world, 0, 1)
