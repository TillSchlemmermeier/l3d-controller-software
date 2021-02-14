import numpy as np
from random import randint, uniform, choice
from multiprocessing import shared_memory

class g_snake():
    '''
    Generator: snake

    A snake!

    Parameters:
    - number   : Number of snakes running around
    - turnprop : propability of doing a turn
    '''

    def __init__(self):
        self.number = 1
        self.turnprop = 0.25

        # create an internal world with i snake point
        self.axis = 0
        self.direction = 1

        self.world = np.zeros([3, 10, 10, 10])
#        self.world[:, randint(0, 9), randint(0, 9), randint(0, 9)] = 1.0
        self.world[:, 4, 4, 4] = 1.0
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0

    def return_values(self):
        return [b'snake', b'turn', b'', b'', b'channel']


    def return_gui_values(self):
        if 4 > self.channel >= 0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = "Trigger"
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.turnprop,2)), '', '', channel),'utf-8')


    def __call__(self, args):
        self.turnprop = 1-args[0]
        self.channel = int(args[3]*5)-1

        world = np.zeros([3,10,10,10])

        # check if S2L is activated
        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            self.turnprop = 1
            if current_volume > 0:
                #choose direction
                oldaxis = self.axis
                while oldaxis == self.axis:
                    self.axis = randint(1, 3)

                self.direction = choice([-1, 1])

        #check for trigger
        elif self.channel == 4:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.turnprop = 0
            else:
                self.turnprop = 1

        # choose direction
        if uniform(0, 1) > self.turnprop:

            oldaxis = self.axis
            while oldaxis == self.axis:
                self.axis = randint(1, 3)

            self.direction = choice([-1, 1])

        world = np.roll(self.world, self.direction, self.axis)
        self.world = world

        return np.clip(world, 0, 1)
