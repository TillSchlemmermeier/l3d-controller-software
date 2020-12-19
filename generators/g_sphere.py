# modules
import numpy as np
from random import randint
from generators.g_sphere_f import gen_sphere
from multiprocessing import shared_memory

# fortran routine is in g_sphere_f.f90

class g_sphere():

    def __init__(self):
        self.size = 2
        self.color = 0
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0


    #Strings for GUI
    def return_values(self):
        return [b'sphere', b'size', b'', b'', b'channel']

    def return_gui_values(self):
        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.size,2)), '', '', channel),'utf-8')



    def __call__(self, args):
        self.size = round(args[0]*10)
        self.channel = int(args[3]*4)-1

        world = np.zeros([3, 10, 10, 10])

        # check if S2L is activated
        if self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                posx = randint(0,9)
                posy = randint(0,9)
                posz = randint(0,9)
            else:
                self.size = 0

        else:
            posx = randint(0,9)
            posy = randint(0,9)
            posz = randint(0,9)

        world[0,:,:,:] = gen_sphere(self.size, posx, posy, posz)
        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        return np.clip(world, 0, 1)
