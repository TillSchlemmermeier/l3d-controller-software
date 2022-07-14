# modules
import numpy as np
from multiprocessing import shared_memory

class e_redblue():
    '''
    Effect: redblue

    '''

    def __init__(self):
        self.speed = 0.5
        self.red = 1.0
        self.green = 0.0
        self.blue = 0.0
        self.step = 0
        self.range = 1.0
        self.mode = 'normal'
        self.channel = 1.0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")


    #strings for GUI
    def return_values(self):
        return [b'redblue', b'speed', b'range', b'', b'channel']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.speed,2)), str(round(self.range,2)), '', ''), 'utf-8')


    def __call__(self, world, args):
        # parse input
        self.speed = args[0]*0.1
        self.range = args[1]* 0.8 + 0.1


        self.red =  np.sin(self.speed*self.step)*0.5*self.range + 0.5
        self.blue = np.cos(self.speed*self.step)*0.5*self.range + 0.5

        world[0, :, :, :] = world[0, :, :, :]*self.red
        world[1, :, :, :] = world[1, :, :, :]*self.green
        world[2, :, :, :] = world[2, :, :, :]*self.blue

        self.step += 1

        return np.clip(world, 0, 1)
