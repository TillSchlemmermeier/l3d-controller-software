import numpy as np
from scipy.ndimage.interpolation import rotate
from random import choice, uniform
from scipy.signal import sawtooth
#from generators.g_shooting_star_f import gen_shooting_star

class g_dots_on_sphere():
    '''
    Generator: orbiter

    generates a rotating/orbiting object

    Parameters:
    - distance osc/swell
    - angle y swell
    - angle z osc

    '''

    def __init__(self):
        self.number_of_dots = 3
        self.radius = 3
        self.theta = 0.1
        self.rho = 0.1
        self.step = 0
        self.dots = []
        self.dots.append(cdot(self.radius))
        self.number_of_frames = 10
        self.speed = 1
        self.direction = 0
        self.current_dot = choice(self.dots)
        self.current_angle = [0, 0.5]

    def return_values(self):
        return [b'dots_on_sphere', b'n dots', b'n frames', b'radius', b'speed']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(self.number_of_dots), str(self.number_of_frames), str(self.radius), str(round(self.speed,2))),'utf-8')


    def __call__(self, args):
        self.number_of_dots = int(args[0]*8)+1
        self.number_of_frames =  int(args[1]*50)+5
        self.radius = 4-int(np.clip(args[2]*4,1,4))
        self.speed = args[3]*30+10

        # generate empty world
        world = np.zeros([3, 10, 10, 10])

        # repopulate list of dots if number has changed
        if self.number_of_dots != len(self.dots):
            self.dots = []
            for i in range(self.number_of_dots):
                self.dots.append(cdot(self.radius))

        for dot in self.dots:
            temp = dot()
            world[0, :, :, :] += temp
            world[1, :, :, :] += temp
            world[2, :, :, :] += temp

        if self.step <= 0:
            self.step =  self.number_of_frames
            self.current_dot = choice(self.dots)
            self.current_angle[0] = uniform(0, self.speed)
            self.current_angle[1] = self.speed-self.current_angle[0]

        self.current_dot.set(self.radius, self.current_angle[0], self.current_angle[1])
        self.step -= 1

        return np.clip(np.clip(world-0.1, 0, 1)*1.1, 0, 1)

class cdot():
    def __init__(self, radius):
        self.radius = radius
        self.polar  = uniform(0, 10)
        self.rho    = uniform(0, 10)

    def set(self, radius, polar, rho):
        self.radius = np.clip(radius, 0, 4)
        self.polar  += polar
        self.rho    += rho

    def __call__(self):

        world = np.zeros([10, 10, 10])
        world[self.radius, self.radius, self.radius] = 1

        world[:, :, :] = rotate(world[:, :, :], self.polar,
                          axes = (1,2), order = 1,
                          mode = 'nearest', reshape = False)

        world[:, :, :] = rotate(world[:, :, :], self.rho,
                          axes = (0,1), order = 1,
                          mode = 'nearest', reshape = False)

        return world
