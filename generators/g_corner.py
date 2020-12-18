
import numpy as np
from multiprocessing import shared_memory

class g_corner():
    '''
    Generator: corner
    '''

    def __init__(self):
        self.size = 0
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0

    #Strings for GUI
    def return_values(self):
        return [b'corner', b'size', b'', b'', b'channel']

    def return_gui_values(self):
        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.size,2)), '', '', channel),'utf-8')


    def __call__(self, args):
        self.size = int(args[0]*2 + 1)
        self.channel = int(args[3]*4)-1

        # create world
        world = np.zeros([3, 10, 10, 10])

        # check if S2L is activated
        if self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            self.size = int(np.clip(4 * current_volume, 0, 4))

        # switch on corners
        world[:,0:self.size,0:self.size,0:self.size] = 1.0
        world[:,0:self.size,0:self.size,10-self.size:] = 1.0
        world[:,0:self.size,10-self.size:,0:self.size] = 1.0
        world[:,10-self.size:,0:self.size,0:self.size] = 1.0
        world[:,0:self.size,10-self.size:,10-self.size:] = 1.0
        world[:,10-self.size:,0:self.size,10-self.size:] = 1.0
        world[:,10-self.size:,10-self.size:,0:self.size] = 1.0
        world[:,10-self.size:,10-self.size:,10-self.size:] = 1.0

        return np.clip(world, 0, 1)
