# modules
import numpy as np
from random import randint, uniform
from colorsys import hsv_to_rgb
from multiprocessing import shared_memory

class g_rising_square():
    '''
    Generator: rising_square

    a square going from bottom to top

    Parameters:
    - speed
    - random color for each square on / Off
    - Pause duration between new squares
    - s2l channel, channel 4 = Trigger mode
    '''

    def __init__(self):
        self.nled = 1
        self.speed = 2
        self.pause = 2
        self.random = 0
        self.flatworld = np.zeros([3, 4,10,10])
        self.step = 0
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0
        self.counter = 0

    #Strings for GUI
    def return_values(self):
        return [b'rising_square', b'speed', b'color', b'pause', b'channel']

    def return_gui_values(self):
        if self.random == 0:
            color = 'off'
        else:
            color = 'on'

        if 4 > self.channel >=0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = 'Trigger'
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(7-self.speed,2)), color, str(round(self.pause,2)), channel),'utf-8')


    def __call__(self, args):
        self.speed = 7-int((args[0]*6))
        self.random = int(round(args[1]))
        self.pause = int(round((args[2]+0.06)*30)+1)
        self.channel = int(args[3]*5)-1

        world = np.zeros([3,10,10,10])

        # check if S2L is activated
        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                if self.random == 0:
                    for i in range(self.nled):
                        self.flatworld[:, :, 9, :] = 1.0

                else:
                    for i in range(self.nled):
                        color = hsv_to_rgb(uniform(0, 1), 1, 1)

                        self.flatworld[0, :, 9, :] = color[0]
                        self.flatworld[1, :, 9, :] = color[1]
                        self.flatworld[2, :, 9, :] = color[2]

        #check if s2l trigger is activated
        elif self.channel == 4:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = 0

            if self.counter < 6 and self.counter % 2 == 0:
                if self.random == 0:
                    for i in range(self.nled):
                        self.flatworld[:, :, 9, :] = 1.0

                else:
                    for i in range(self.nled):
                        color = hsv_to_rgb(uniform(0, 1), 1, 1)
                        for i in range(3):
                            self.flatworld[i, :, 9, :] = color[i]

                self.counter += 1


        elif self.step % self.pause == 0:
            if self.random == 0:
                for i in range(self.nled):
                    self.flatworld[:, :, 9, :] = 1.0

            else:
                for i in range(self.nled):
                    color = hsv_to_rgb(uniform(0, 1), 1, 1)

                    self.flatworld[0, :, 9, :] = color[0]
                    self.flatworld[1, :, 9, :] = color[1]
                    self.flatworld[2, :, 9, :] = color[2]

        world[:, :, :, 0] = self.flatworld[:, 0, :, :]
        world[:, :, 9, :] = self.flatworld[:, 1, :, :]
        world[:, :, :, 9] = self.flatworld[:, 2, :, :]
        world[:, :, 0, :] = self.flatworld[:, 3, :, :]



        if self.step % self.speed == 0:
            self.flatworld = np.roll(self.flatworld, shift = -1, axis = 2)
            self.flatworld[:, :, 9, :] = 0.0

        self.step += 1

        return np.clip(world, 0, 1)
