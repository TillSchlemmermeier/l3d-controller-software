# modules
import numpy as np
from random import choice, uniform
from generators.g_torusrotation import g_torusrotation
from generators.g_growing_sphere import g_growing_sphere
from colorsys import rgb_to_hsv, hsv_to_rgb

class a_pulsating_torus():
    '''
    Automat: pulsating torus

    the torus should rotate all the time, in blue
    '''

    def __init__(self):

        # initialize torus
        self.torus = g_torusrotation()
        self.torus.control([0.0, 0.0, 0.0])

        # initialize growing_sphere
        self.sphere = g_growing_sphere()
        self.sphere.control([0.0, 0.1, 0.0])

        # we have two oscillations
        # 1: size of sphere
        # 2: fade of torus

        self.blue =  hsv_to_rgb(240/360.0, 1.0, 1.0)
        self.red =  hsv_to_rgb(24/360.0, 1.0, 1.0)
        self.orange =  hsv_to_rgb(48/360.0, 1.0, 1.0)

    def control(self, count_fade, start_strobo, blub1):
        self.period = int(count_fade * 200)+50
        self.start_strobo = int(start_strobo*10 +1)

    def label(self):
        return ['frames per fade', self.period,
                'cycles before strobo', self.start_strobo,
                'empty', 'empty']

    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

        size = np.abs(np.sin(self.counter / self.period * np.pi))*6
        brightness  = np.sin(self.counter / self.period * np.pi)**4

        world[0, :, :, :] = np.clip(gen_hsphere(size, 4.5, 4.5, 4.5),0,1) * brightness
        world[1:, :, :, :] = world[0, :, :, :]
        world[2:, :, :, :] = world[0, :, :, :]

        # color
        if self.counter % self.period == 0:
            self.color =  hsv_to_rgb(uniform(-0.5,0.5), 1.0, 1.0)

        world[0,:,:,:] *= self.color[0]
        world[1,:,:,:] *= self.color[1]
        world[2,:,:,:] *= self.color[2]

        if self.counter > self.start_strobo*self.period:
            size = 6
            if self.counter % 2 == 0:
                world[0, :, : ,:] = gen_hsphere(size, 4.5, 4.5, 4.5) * self.strobo_bright**6
                world[1, :, :, :] = world[0, :, :, :]
                world[2, :, :, :] = world[0, :, :, :]

            self.strobo_bright += 1/self.strobo_counter
#            size += 1/self.strobo_counter

        if self.counter >= self.start_strobo*self.period+self.strobo_counter:
            self.counter = -1
            self.strobo_bright = 0

        self.counter += 1

        return np.clip(world, 0, 1)
