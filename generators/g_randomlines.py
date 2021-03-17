# modules
import numpy as np
from random import randint, uniform
from colorsys import hsv_to_rgb
from multiprocessing import shared_memory


class g_randomlines():
    '''
    Generator: randomlines

    a random line

    Parameters:
    - wait time
    - random color for each line on / Off
    - s2l channel, channel 4 = Trigger mode
    '''

    def __init__(self):
        self.reset = 1
        self.counter = 0
        self.saveworld = np.zeros([3,10,10,10])
        self.randomcolor = 0
        # s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0
        self.step = 0
        self.linelist = []

    def return_values(self):
        return [b'randomlines', b'wait', b'Color', b'', b'channel']

    def return_gui_values(self):
        if self.randomcolor == 0:
            color = 'off'
        else:
            color = 'on'

        if 4 > self.channel >=0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = 'Trigger'
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.reset,2)), color, '', channel),'utf-8')

    def __call__(self, args):
        self.reset = int(args[0]*10)+1
        self.randomcolor = int(round(args[1]))
        self.channel = int(args[3]*5)-1

        world = np.zeros([3, 10, 10, 10])

        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                direction = randint(0, 2)
                if direction == 0:
                    world[:, :, randint(0, 9), randint(0, 9)] = 1
                elif direction == 1:
                    world[:, randint(0, 9), :, randint(0, 9)] = 1
                elif direction == 2:
                    world[:, randint(0, 9), randint(0, 9), :] = 1

                if self.randomcolor == 1:
                    color = hsv_to_rgb(uniform(0, 1), 1, 1)
                    for i in range(3):
                        world[i, :, :, :] *= color[i]

        elif self.channel == 4:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.step = 0
                self.linelist.clear()
                self.saveworld[:, :, :, :] = 0

                for i in range(self.reset):
                    direction = randint(0, 2)
                    a = randint(0, 9)
                    b = randint(0, 9)
                    if direction == 0:
                        world[:, :, a, b] = 1
                    elif direction == 1:
                        world[:, a, :, b] = 1
                    elif direction == 2:
                        world[:, a, b, :] = 1

                    self.linelist.extend([direction, a, b])

                    if self.randomcolor == 1:
                        color = hsv_to_rgb(uniform(0, 1), 1, 1)
                        for i in range(3):
                            world[i, :, :, :] *= color[i]

            if self.step < self.reset:
                try:
                    direction = self.linelist[3*self.step]
                    a = self.linelist[3*self.step + 1]
                    b = self.linelist[3*self.step + 2]

                except:
                    direction = 0
                    a = 0
                    b = 0

                if direction == 0:
                    world[:, :, a, b] = 1
                elif direction == 1:
                    world[:, a, :, b] = 1
                elif direction == 2:
                    world[:, a, b, :] = 1

                if self.randomcolor == 1:
                    color = hsv_to_rgb(uniform(0, 1), 1, 1)
                    for i in range(3):
                        world[i, :, :, :] *= color[i]


                self.step += 1


        elif self.counter % self.reset == 0:
            direction = randint(0, 2)
            if direction == 0:
                world[:, :, randint(0, 9), randint(0, 9)] = 1
            elif direction == 1:
                world[:, randint(0, 9), :, randint(0, 9)] = 1
            elif direction == 2:
                world[:, randint(0, 9), randint(0, 9), :] = 1

            if self.randomcolor == 1:
                color = hsv_to_rgb(uniform(0, 1), 1, 1)
                for i in range(3):
                    world[i, :, :, :] *= color[i]

        else:
            world = self.saveworld

        self.counter += 1

        self.saveworld = world
        return np.clip(world, 0, 1)
