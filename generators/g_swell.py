
import numpy as np
from scipy.signal import sawtooth
from generators.g_shooting_star_f import gen_shooting_star
from random import randint
from multiprocessing import shared_memory

class g_swell():

    def __init__(self):
        self.pos1 = [randint(2,8), randint(2,8), randint(2,8)]
        self.pos2 = [randint(2,8), randint(2,8), randint(2,8)]
        self.speed = 0.1
        self.counter = 0
        self.brightness = 0.0
        self.dir = 1.0
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0


    #Strings for GUI
    def return_values(self):
        return [b'swell', b'speed', b'', b'', b'channel']

    def return_gui_values(self):
        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.speed,2)), '', '', channel),'utf-8')


    def __call__(self, args):

        # parse parameters
        self.speed = args[0]+0.05
        self.channel = int(args[3]*4)-1

        # generate empty world
        world1 = np.zeros([10, 10, 10])
        world2 = np.zeros([10, 10, 10])
        world = np.zeros([3, 10, 10, 10])

        # check if S2L is activated
        if self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                self.speed = current_volume

        # create new point
        if self.brightness <= 0.0:
            self.counter = 0
            self.pos = [randint(2,8), randint(2,8), randint(2,8)]
            self.dir *= -1
            self.pos1 = [randint(2,8), randint(2,8), randint(2,8)]

        # change direction
        if self.brightness >= 1.0:
            self.dir *= -1
            self.pos2 = [randint(2,8), randint(2,8), randint(2,8)]

        self.brightness = np.clip(self.brightness+ self.dir*self.speed, 0, 1)

        world1[:, :, :] = gen_shooting_star(self.pos1[0],
                                           self.pos1[1],
                                           self.pos1[2])

        world2[:, :, :] = gen_shooting_star(self.pos2[0],
                                           self.pos2[1],
                                           self.pos2[2])


        world[0,:,:,:] = world1*self.brightness + world2*(1.0-self.brightness)
        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        return np.clip(world, 0, 1)
