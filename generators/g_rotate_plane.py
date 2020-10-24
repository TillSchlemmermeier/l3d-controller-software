# modules
import numpy as np
from scipy.ndimage.interpolation import rotate
from multiprocessing import shared_memory
from random import randint

class g_rotate_plane():
    def __init__(self):
        self.original = np.zeros([10,10,10])
        for i in range(8):
            self.original[4:5, 1:-1, 1:-1] = 1

        self.xspeed = 0.1
        self.yspeed = 0.1
        self.zspeed = 0.0
        self.step = 0
        self.axe = 0

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0

    #Strings for GUI
    def return_values(self):
        return [b'rotate_plane', b'xspeed', b'yspeed', b'zspeed', b'channel']


    def return_gui_values(self):
        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.xspeed,2)), str(round(self.yspeed,2)), str(round(self.zspeed,2)), channel),'utf-8')


    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.xspeed = 20*args[0]
        self.yspeed = 20*args[1]
        self.zspeed = 20*args[2]
        self.channel = int(args[3]*4)-1

        # create world
        world = np.zeros([3, 10, 10, 10])

        # check if S2L is activated
        if self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
                if current_volume > 0:
                self.axe = randint(0, 3)
                    if self.axe == 0:
                        self.xpeed = 20*current_volume
                    if self.axe == 1:
                        self.yspeed = 20*current_volume
                    if self.axe == 2:
                        self.zspeed =20*current_volume

        # rotate
        newworld = rotate(self.original, self.step*self.xspeed,
                          axes = (1,2), order = 1,
	                      mode = 'nearest', reshape = False)

        newworld = rotate(newworld, self.step*self.yspeed,
                          axes = (0,1), order = 1,
	                      mode = 'nearest', reshape = False)

        newworld = rotate(newworld, self.step*self.zspeed,
                          axes = (0,2), order = 1,
	                      mode = 'nearest', reshape = False)


        # insert array
        world[0, :, :, :] = newworld
        world[1, :, :, :] = newworld
        world[2, :, :, :] = newworld

        self.step += 1

        return np.clip(world, 0, 1)
