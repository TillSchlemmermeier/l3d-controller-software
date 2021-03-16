# modules
import numpy as np
from random import randint, uniform
from colorsys import hsv_to_rgb
from multiprocessing import shared_memory


class g_sound_lines():
    '''
    Generator: sound_lines

    Generate random vertical lines when triggered by sound

    Parameters:
    - wait time
    - random color for each square on / Off
    - Pause duration between new squares
    - s2l channel, channel 4 = Trigger mode
    '''

    def __init__(self):

        self.number = 10
        # get initial random lines
        self.lines = []
        for i in range(self.number):
            self.lines.append([slice(0, 10, 1), randint(0, 9), randint(0, 9)])

        self.counter = 1
        self.reset = 20
        self.randomcolor = 0
        self.spectrum = 0
        # s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.lastvalue = 0


    def return_values(self):
        return [b'sound_lines', b'number', b'Wait', b'Color', b'Channel']


    def return_gui_values(self):
        if 4 > self.channel:
            channel = str(self.channel)
        else:
            channel = 'Trigger'

        if self.randomcolor == 0:
            color = 'off'
        else:
            color = 'on'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.number,2)), str(round(self.reset,2)), color, channel),'utf-8')


    def __call__(self, args):

        # process parameters
        self.number = int(args[0]*15)
        self.reset = args[1]*20+1
        self.randomcolor = int(round(args[2]))
        self.channel = int(args[3]*4)

        # now we can world with the sound
        world = np.zeros([3, 10, 10, 10])

        if self.channel == 4:
            current_volume = int(float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.spectrum = uniform(0,1)
                self.lines = []
                for i in range(self.number):
                    self.lines.append([slice(0, 10, 1), randint(0, 9), randint(0, 9)])

                # get lines
                for line in self.lines:
                    world[:, line[0], line[1], line[2]] = current_volume

                    if self.randomcolor == 1:
                        low = np.clip(self.spectrum - 0.08, 0, 1)
                        high = np.clip(self.spectrum + 0.08, 0, 1)
                        color = hsv_to_rgb(uniform(low, high), 1, 1)
                        for i in range(3):
                            world[i, :, :, :] *= color[i]


        elif self.channel < 4:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))

            # get lines
            for line in self.lines:
                world[:, line[0], line[1], line[2]] = current_volume

                if self.randomcolor == 1:
                    low = np.clip(self.spectrum - 0.08, 0, 1)
                    high = np.clip(self.spectrum + 0.08, 0, 1)
                    color = hsv_to_rgb(uniform(low, high), 1, 1)
                    for i in range(3):
                        world[i, :, :, :] *= color[i]

            if self.counter > self.reset:
                self.spectrum = uniform(0,1)
                self.lines = []
                # reset lines
                for i in range(self.number):
                    self.lines.append([slice(0, 10, 1), randint(0, 9), randint(0, 9)])

                self.counter = 0

            self.counter += 1


        return np.round(np.clip(world, 0, 1), 3)
