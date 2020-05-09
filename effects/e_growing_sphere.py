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
        self.step = 0

    #strings for GUI
    def return_values(self):
        return [b'growing_sphere', b'amount', b'growspeed', b'oscillate (sin/sawtooth)', b'']


    def __call__(self, world, args):
        # parsing input
        self.amount = args[0]
        self.growspeed = args[1]
        self.oscillate = args[2]

        # oscillates between 0 and 1
        if self.oscillate < 0.5:
            osci = np.sin(self.step*self.growspeed)*0.5 + 0.5
        else:
            osci = sawtooth(self.step*self.growspeed)*0.5 + 0.5

        # scales to maxsize
        size = self.maxsize * osci

        self.step += 1

        # creates hollow sphere with parameters
        world[0, :, :, :] = world[0, :, :, :] * (self.amount + np.clip(gen_hsphere(size, 4.5, 4.5, 4.5),0,1))
        world[1, :, :, :] = world[1, :, :, :] * (self.amount + np.clip(gen_hsphere(size, 4.5, 4.5, 4.5),0,1))
        world[2, :, :, :] = world[2, :, :, :] * (self.amount + np.clip(gen_hsphere(size, 4.5, 4.5, 4.5),0,1))

        return np.clip(world, 0, 1)


def hsphere(radius):

    world = np.zeros([10, 10, 10])

    for x in range(10):
        for y in range(10):
            for z in range(10):
                dist = np.sqrt((x-4.5)**2+(y-4.5)**2+(z-4.5)**2)
                world[x, y, z] = 1.0/(radius-dist+0.0001)**8

    return np.round(np.clip(world, 0, 1), 3)
