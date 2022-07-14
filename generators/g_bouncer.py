import numpy as np
from scipy.signal import sawtooth
from generators.g_genhsphere import gen_hsphere


class g_bouncer():

    def __init__(self):
        self.double = False
        self.speed  = 0.1
        self.step = 0

    def return_values(self):
        return [b'bouncer', b'double', b'speed', b'', b'']

    def return_gui_values(self):
        if self.double:
            text = 'double'
        else:
            text = 'single'
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(text, str(round(self.speed,2)), '', ''),'utf-8')


    #def generate(self, step, dumpworld):
    def __call__(self, args):
        if args[0] > 0.5:
            self.double = True
        else:
            self.double = False

        self.speed = args[1]**2

        # generate empty world
        world = np.zeros([3, 10, 10, 10])

        # get position
        position = 4.5 + 5*(np.sin(self.step * self.speed)**2)

        # switch on leds depending on distance
        world[0,:,:,:] = gen_hsphere(0.01, 4.5, 4.5, position)
        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        if self.double == True:
            tempworld = np.zeros([3, 10, 10, 10])
            tempworld[:, :, :, :] = world[:, :, :, :]
            world[:, :, :, :] += tempworld[:, :, :, ::-1]

        self.step += 1

        return world**2
