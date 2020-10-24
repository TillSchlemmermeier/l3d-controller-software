import numpy as np
from scipy.signal import sawtooth
from multiprocssing import shared_memory

class g_squares():

    def __init__(self):
        self.speed = 10
        self.dir = 1
        self.type = 0
        self.step = 0

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0

    #Strings for GUI
    def return_values(self):
        return [b'squares', b'speed', b'dir', b'type', b'channel']

    def return_gui_values(self):
        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        if self.dir == 0:
            dir = 'X'
        elif self.dir == 1:
            dir ='Y'
        else:
            dir = 'Z'

        if self.type < 0.33:
            type = 'sin'
        elif self.type >= 0.33 and self.type < 0.66:
            type = 'up'
        else:
            type = 'down'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.speed,2)), dir, type, channel),'utf-8')



    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.speed = int(args[0]*9)
        self.dir = int(round(args[1]*3))
        self.type = args[2]
        self.channel = int(args[3]*4)-1

    #def generate(self, step, dumpworld):
        world = np.zeros([3, 10, 10, 10])
        if self.type < 0.33:
            position = int( round((np.sin(0.1*self.step*self.speed)+1)*4.5))
        elif self.type >= 0.33 and self.type < 0.66:
            position = int( round((sawtooth(0.1*self.step*self.speed)+1)*4.5))
        else:
            position = int( round((sawtooth(0.1*self.step*self.speed, width=0)+1)*4.5))

        if self.dir == 0:
            world[:, position,:,:] = 1.0
            world[:, :, 1:-1, 1:-1] = 0.0
        elif self.dir == 1:
            world[:, :, position,:] = 1.0
            world[:, 1:-1, :, 1:-1] = 0.0
        else:
            world[:, :,:,position] = 1.0
            world[:, 1:-1, 1:-1, :] = 0.0

        # check if S2L is activated
        if self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0
                self.step += 1
        else:
            self.step += 1

        return world
