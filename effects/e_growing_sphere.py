# modules
import numpy as np
from scipy.signal import sawtooth
from generators.g_genhsphere import gen_hsphere

class e_growing_sphere():

    def __init__(self):
        self.maxsize = 10
        self.growspeed = 1
        self.amount = 0.5
        self.oscillate = 0

    def label(self):
        return ['rest brightness',round(self.amount,2),'growspeed',round(self.growspeed,2),'oscillate',round(self.oscillate,2)]

    def control(self, amount, growspeed, oscillate):
        self.amount = amount
        self.growspeed = growspeed
        self.oscillate = oscillate

    def generate(self, step, dumpworld):
        world = dumpworld

        # oscillates between 0 and 1
        if self.oscillate < 0.5:
            osci = np.sin(step*self.growspeed)*0.5 + 0.5
        else:
            osci = sawtooth(step*self.growspeed)*0.5 + 0.5

        # scales to maxsize
        size = self.maxsize * osci

        # creates hollow sphere with parameters
        world[0, :, :, :] = world[0, :, :, :] * (self.amount + np.clip(gen_hsphere(size, 4.5, 4.5, 4.5),0,1))
        world[1, :, :, :] = world[1, :, :, :] * (self.amount + np.clip(gen_hsphere(size, 4.5, 4.5, 4.5),0,1))
        world[2, :, :, :] = world[2, :, :, :] * (self.amount + np.clip(gen_hsphere(size, 4.5, 4.5, 4.5),0,1))

        return np.clip(world,0,1)


def hsphere(radius):

    world = np.zeros([10, 10, 10])

    for x in range(10):
        for y in range(10):
            for z in range(10):
                dist = np.sqrt((x-4.5)**2+(y-4.5)**2+(z-4.5)**2)
                world[x, y, z] = 1.0/(radius-dist+0.0001)**8

    return np.round(np.clip(world, 0, 1), 3)
