import numpy as np
from multiprocessing import shared_memory

class g_corner_grow():
    '''
    Generator: corner_grow

    '''

    def __init__(self):
        self.waiting = 10
        self.size = 0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.waitingcounter = 0

    #Strings for GUI
    def return_values(self):
        return [b'corner_grow', b'waiting', b'', b'', b'channel']

    def return_gui_values(self):
        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.waiting,2)), '', '', channel),'utf-8')


    def __call__(self, args):
        self.waiting = int(args[0]*50)
        self.channel = int(args[3]*4)-1

        # create world
        world = np.zeros([3, 10, 10, 10])

        if self.size > 4.0:
            # switch into waiting state
            self.waitingcounter = self.waiting
            self.size = 0

            # check if S2L is activated
            if self.channel >= 0:
                current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
                if current_volume > 0:
                    self.waitingcounter == 0

        elif self.waitingcounter == 0:
        # switch on corners
            world[:,4-self.size,4-self.size,4-self.size] = 1.0
            world[:,4-self.size,4-self.size,5+self.size] = 1.0
            world[:,4-self.size,5+self.size,4-self.size] = 1.0
            world[:,5+self.size,4-self.size,4-self.size] = 1.0
            world[:,4-self.size,5+self.size,5+self.size] = 1.0
            world[:,5+self.size,4-self.size,5+self.size] = 1.0
            world[:,5+self.size,5+self.size,4-self.size] = 1.0
            world[:,5+self.size,5+self.size,5+self.size] = 1.0

            self.size += 1

        else:
            # stay in waiting state
            self.waitingcounter -= 1

        return np.clip(world, 0, 1)
