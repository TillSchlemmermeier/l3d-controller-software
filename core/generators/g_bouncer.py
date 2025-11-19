import numpy as np
from scipy.signal import sawtooth
from generators.g_genhsphere import gen_hsphere


class g_bouncer():

    def __init__(self):
        self.double = False
        self.speed  = 0.1
        self.step = 0

    def return_state(self):
        return [
            ['mode', 'double', 'double' if self.double else 'single'],
            ['speed', 'speed', round(self.speed,2)],
        ]
    
    def __call__(self, args):
        # === PARAMETERS START ===
        self.double = args[0] > 0.5
        self.speed = args[1]**2
        # === PARAMETERS END ===

        # generate empty world
        world = np.zeros([3, 10, 10, 10])

        # get position
        position = 4.5 + 5*(np.sin(self.step * self.speed)**2)

        # switch on leds depending on distance
        world[0,:,:,:] = gen_hsphere(0.01, 4.5, 4.5, position)
        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        if self.double:
            tempworld = np.zeros([3, 10, 10, 10])
            tempworld[:, :, :, :] = world[:, :, :, :]
            world[:, :, :, :] += tempworld[:, :, :, ::-1]

        self.step += 1

        return world**2
