import numpy as np
from scipy.signal import sawtooth
from multiprocessing import shared_memory

class g_squares():
    '''
    Generator: squares
    a square moving up and down the edges

    Parameters:
    speed
    direction (x, y or z)
    type (sinus, up or down)
    Sound2Light channel
    '''

    def __init__(self):
        self.speed = 10
        self.dir = 1
        self.type = 0
        self.step = 0

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0

    #Strings for GUI
    def return_values(self):
        return [b'squares', b'speed', b'dir', b'type', b'channel']

    def return_gui_values(self):
        if 4 > self.channel >= 0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = "Trigger"
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
        self.channel = int(args[3]*5)-1

    #def generate(self, step, dumpworld):
        world = np.zeros([3, 10, 10, 10])
        if self.type < 0.33:
            position = int( round((np.sin(0.1*self.step*self.speed)+1)*4.5))
        elif self.type >= 0.33 and self.type < 0.66:
            position = int( round((sawtooth(0.1*self.step*self.speed)+1)*4.5))
        else:
            position = int( round((sawtooth(0.1*self.step*self.speed, width=0)+1)*4.5))

        # check if S2L is activated
        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            current_volume = int(current_volume*6)

            if self.dir == 0:
                world[:, position-current_volume:position,4-current_volume:4+current_volume,4-current_volume:4+current_volume] = 1.0
                world[:, :, 1:-1, 1:-1] = 0.0
            elif self.dir == 1:
                world[:, 4-current_volume:current_volume, position-current_volume:position,4-current_volume:4+current_volume] = 1.0
                world[:, 1:-1, :, 1:-1] = 0.0
            else:
                world[:, 4-current_volume:4+current_volume,4-current_volume:4+current_volume,position-current_volume:position] = 1.0
                world[:, 1:-1, 1:-1, :] = 0.0

        else:
            if self.dir == 0:
                world[:, position,:,:] = 1.0
                world[:, :, 1:-1, 1:-1] = 0.0
            elif self.dir == 1:
                world[:, :, position,:] = 1.0
                world[:, 1:-1, :, 1:-1] = 0.0
            else:
                world[:, :,:,position] = 1.0
                world[:, 1:-1, 1:-1, :] = 0.0


        #check for trigger
        if self.channel == 4:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.step = 0

            if self.step < self.speed:
                self.step += 1

        else:
            self.step += 1

        return world
