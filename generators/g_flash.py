# modules
import numpy as np
from random import choice, randint
from multiprocessing import shared_memory

class g_flash():

    def __init__(self):
        self.counter = 0
        self.points = self.gen_line()
        self.reset = 11
        self.wait = 4
        self.speed = 1

        self.trigger = False

        # s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0

    #Strings for GUI
    def return_values(self):
        return [b'flash', b'speed', b'wait', b'', b'trigger']

    def return_gui_values(self):
        if self.trigger:
            channel = 'yes'
        else:
            channel = 'no'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(self.speed), str(self.wait), '', channel),'utf-8')


    def __call__(self, args):

        self.speed = int(round(args[0]*1))+1
        self.wait = int(round(args[1]*20))
        if args[3] > 0.5:
            self.trigger = True
        else:
            self.trigger = False

        # create world
        world = np.zeros([3, 10, 10, 10])

        current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))

        # check if S2L is activated
        '''
        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                if self.brightness <=1.0:
                    world[0, self.edge[0], self.edge[1], self.edge[2]] = self.brightness**2
                    self.brightness += current_volume
                else:
                    self.edge = choice(self.edge_list)
                    self.brightness = 0
        '''

        if 0 < self.counter < self.reset:
            self.lastvalue = current_volume
            for i in range(self.speed):
                for step in range(self.counter):
                    world[0, self.points[step][0], self.points[step][1], self.points[step][2]] = 1

                self.counter += 1

        elif self.reset <= self.counter < self.reset + 2:
            self.lastvalue = current_volume
            self.counter += 1

        elif self.reset + 2 <= self.counter < self.reset + 4:
            for p in self.points:
                world[0, p[0], p[1], p[2]] = 1
            self.counter += 1

        elif self.counter >= self.reset + 4 and not self.trigger:
            # reset
            self.counter = -self.wait
            self.points = self.gen_line()
        elif self.counter >= self.reset +4 and self.trigger and current_volume > self.lastvalue:
            # reset with trigger
            self.lastvalue = current_volume
            self.counter = -self.wait
            self.points = self.gen_line()
        else:
            self.counter += 1

        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        return np.clip(world, 0, 1)

    def gen_line(self):

        points = []
        points.append([0, randint(0,9), randint(0,9)])

        for i in range(1,10):
            y = np.clip(points[-1][1] + choice([-1,0,1]), 0, 9)
            z = np.clip(points[-1][2] + choice([-1,0,1]), 0, 9)
            points.append([i, y, z])


        return points
