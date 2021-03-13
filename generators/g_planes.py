# modules
import numpy as np
from scipy.signal import sawtooth
from multiprocessing import shared_memory

class g_planes():
    '''
    Generator: random

    Moves planes through the cube
    '''
    def __init__(self):
        self.speed = 10
        self.dir = 1
        self.type = 0
        self.step = 0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 4
        self.lastvalue = 0
        self.oldposition = 0
        self.switch = False
        self.stop = False

        #dict for dir
        self.dict = {0: 'X+',
                     1: 'Y+',
                     2: 'Z+',
                     3: 'X-',
                     4: 'Y-',
                     5: 'Z-'}

    #Strings for GUI
    def return_values(self):
        return [b'planes', b'speed', b'direction', b'type', b'channel']

    def return_gui_values(self):
        direction = self.dict[self.dir]
        if self.type == 0.5:
            type = 'saw'
        else:
            type = 'triangle'

        if 4 > self.channel >=0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = 'Trigger'
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.speed,2)), direction, type, channel),'utf-8')


    def __call__(self, args):
        # parsing input
        self.speed = args[0]*10
        self.dir = int(round(args[1]*5))
        if args[2] > 0.5:
            self.type = 0.5
        else:
            self.type = 1.0

        self.channel = int(args[3]*5)-1

        # calculate frame
        world = np.zeros([3, 10, 10, 10])
        position = int(round((sawtooth(0.1*self.step*self.speed, self.type)+1)*4.51))

        # check if s2l is activated
        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                if self.dir < 3:
                    self.step += 1
                else:
                    self.step-= 1

        # check if s2l trigger is activated
        elif self.channel == 4:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.switch = False
                self.stop = False
                self.step = 0
                self.oldposition = 0

            if self.type == 0.5:
                if position < self.oldposition:
                    self.switch = True

                if self.switch:
                    if position > self.oldposition:
                        self.stop = True

            elif self.type == 1:
                if position < self.oldposition:
                    self.stop = True

            if not self.stop:
                if self.dir < 3:
                    self.step += 1
                else:
                    self.step-= 1

            self.oldposition = position

        else:
            if self.dir < 3:
                self.step += 1
            else:
                self.step-= 1

        if self.dir == 0 or self.dir == 3:
            world[:, position,:,:] = 1.0
        elif self.dir == 1 or self.dir == 4:
            world[:, :, position,:] = 1.0
        else:
            world[:, :,:,position] = 1.0

        if self.channel == 4:
            if self.stop:
                world[:, :, :, :] = 0.0

        return np.clip(world, 0, 1)
