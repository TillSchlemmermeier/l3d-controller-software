# modules
import numpy as np
from scipy.stats import multivariate_normal

class wave():

    def __init__(self):
        self.sigma = 1
        self.amplitude = 30
        self.speed = 1
        self.counter = 0

    def control(self, sigma, amplitude, speed):
        self.sigma = sigma*5+1
        self.amplitude = amplitude*50
        self.speed = speed

    def label(self):
        return ['sigma',round(self.sigma,2),'amplitude',round(self.amplitude,2), 'speed',round(self.speed,2),'empty','empty']

    def generate(self, step, dumpworld):

        world = np.zeros([3, 10, 10, 10])


        a = np.zeros([10,10])

        if self.counter > 15:
            self.direction = randint(1,8)
            self.position = randint(0,9)

            self.counter = 0

        i = self.counter
        direction = self.direction
        position = self.position

        if direction == 1: #x+
            for x in range(10):
    #            a[x,:] = ((np.sin((i)/np.pi + x/np.pi)+1)/2)**4
                a[x,:] = np.exp(-((x+5-i)**2)/10)
            world[:,:,position] = a
        elif direction == 2: #x-
            for x in range(10):
                a[x,:] = np.exp(-((x-15+i)**2)/10)
                world[:,:,position] = a
        elif direction == 3: #y+
            for y in range(10):
                a[:,y] = np.exp(-((y+5-i)**2)/10)
            world[:,:,position] = a
        elif direction == 4: #y-
            for y in range(10):
                a[:,y] = np.exp(-((y-15+i)**2)/10)
            world[:,:,position] = a
        elif direction == 5: #xy
            for x in range(10):
                for y in range(10):
                    a[x,y] = np.exp(-((x+y-25+i)**2)/10) # done
            world[:,:,position] = a
        elif direction == 6: #x-y
            for x in range(10):
                for y in range(10):
                    a[x,y] = np.exp(-((x-y+15-i)**2)/10) # done
            world[:,:,position] = a
        elif direction == 7: #-xy
            for x in range(10):
                for y in range(10):
                    a[x,y] = np.exp(-((-x+y+15-i)**2)/10)
            world[:,:,position] = a
        elif direction == 8: #-x-y
            for x in range(10):
                for y in range(10):
                    a[x,y] = np.exp(-((-x-y+25-i)**2)/10)
            world[:,:,position] = a

        self.counter += 1
        return np.clip(world, 0, 1)
