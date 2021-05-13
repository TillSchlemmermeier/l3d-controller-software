import numpy as np
from random import uniform
from generators.g_shooting_star_f import gen_shooting_star
from multiprocessing import shared_memory

class g_shooting_star():

    def __init__(self):
        # default parameter
        self.counter = 1
        self.steps = 4
        self.mode = 'in'
        self.add_wait = 4

        self.dot_list = []
        self.dot_list.append(gen_line_2(self.steps, self.mode))
        # s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0

    def return_values(self):
        return [b'shooting star', b'wait frames', b'speed', b'mode', b'channel']

    def return_gui_values(self):
        if 4 > self.channel >= 0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = "Trigger"
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(self.add_wait), str(20-self.steps), self.mode, channel),'utf-8')

    def __call__(self, args):
        self.add_wait = int(args[0]*10+1)
        self.steps = 20-int(args[1]*18)
        if args[2] < 0.25:
            self.mode = 'in'
        elif args[2] > 0.25 and args[2] < 0.5:
            self.mode = 'out'
        elif args[2] > 0.5 and args[2] < 0.75:
            self.mode = 'through'
        else:
            self.mode = 'top'
        self.channel = int(args[3]*5)-1

        world = np.zeros([3, 10, 10, 10])

        # check if S2L is activated
        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                self.dot_list.insert(0, gen_line_2(self.steps, self.mode))

        #check for trigger
        elif self.channel == 4:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.dot_list.insert(0, gen_line_2(self.steps, self.mode))

        # add new dot
        elif self.counter % self.add_wait == 0:
            self.dot_list.insert(0, gen_line_2(self.steps, self.mode))

        self.counter += 1

        delete_last = False
        for i in range(len(self.dot_list)):
            try:
                tempworld = np.zeros([10, 10, 10])
                tempworld = gen_shooting_star(self.dot_list[i][0][0],
                                              self.dot_list[i][0][1],
                                              self.dot_list[i][0][2])
                world[0, :, :, :] += tempworld
                del self.dot_list[i][0]

                if len(self.dot_list[i]) < 1:
                    delete_last = True

            except:
                pass

        if delete_last:
            del(self.dot_list[-1])

        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        return np.clip(world, 0, 1)


def gen_line_2(steps, mode):
    if mode == 'out':
        p1 = [4.5, 4.5 ,4.5]
        p2 = polar2z(10, uniform(0, np.pi), uniform(0, 2*np.pi))
        p2[0] += 4.5
        p2[1] += 4.5
        p2[2] += 4.5

    elif mode == 'top':
        p2 = [10, uniform(-1, 10),uniform(-1, 10)]
        p1 = [-1, uniform(4, 5),uniform(4, 5)]

    else:
        p2 = [4.5, 4.5 ,4.5]
        p1 = polar2z(10, uniform(0, np.pi), uniform(0, 2*np.pi))
        p1[0] += 4.5
        p1[1] += 4.5
        p1[2] += 4.5

    if mode == 'through':
        v = [2*(p2[0] - p1[0]), 2*(p2[1] - p1[1]), 2*(p2[2] - p1[2])]
    else:
        v = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]

    coords = []
    for i in range(steps):
        coords.append([p1[0]+i*v[0]/steps, p1[1]+i*v[1]/steps, p1[2]+i*v[2]/steps])

    return coords

def polar2z(r, theta, phi):
    # polar coordinates to cartesian
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return [x, y, z]
