# modules
import numpy as np
from random import randint
from multiprocessing import shared_memory

class g_trees():
    '''
    Generator: trees

    Trees growing from the bottom

    Parameters:
    - number of LEDs
    - Speed
    - Frames before reset
    '''

    def __init__(self):
        self.nled = 1
        self.speed = 2
        self.flatworld = np.zeros([4,10,10])
        self.step = 0
        self.reset = 1
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.trigger = False
        self.lastvalue = 0


    #Strings for GUI
    def return_values(self):
        return [b'trees', b'N LEDs', b'speed', b'wait', b'Trigger']

    def return_gui_values(self):
        if self.trigger:
            trigger = 'On'
        else:
            trigger = "Off"

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.nled,2)), str(round(self.speed,2)), str(round(self.reset,2)), trigger),'utf-8')

    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.nled = int(round(args[0]*4)+1)
        self.speed = 5-int((args[1]*4))
        self.reset = int(args[2]*5+1)
        if args[3] > 0.2:
            self.trigger = True
        else:
            self.trigger = False

        world = np.zeros([3,10,10,10])

        if self.trigger:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                for i in range(self.nled):
                    self.flatworld[randint(0,3), 9, randint(0,9)] = 1.0


        elif self.step % self.reset == 0:
            for i in range(self.nled):
                self.flatworld[randint(0,3), 9, randint(0,9)] = 1.0


        world[0, :, :, 0] = self.flatworld[0, :, :]
        world[0, :, 9, :] = self.flatworld[1, :, :]
        world[0, :, :, 9] = self.flatworld[2, :, :]
        world[0, :, 0, :] = self.flatworld[3, :, :]

        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        if self.step % self.speed == 0:
            self.flatworld = np.roll(self.flatworld, shift = -1, axis = 1)
            self.flatworld = np.roll(self.flatworld, shift = randint(-1,1), axis = 2)

            self.flatworld[:, 9, :] = 0.0

        self.step += 1
        return np.clip(world, 0, 1)
