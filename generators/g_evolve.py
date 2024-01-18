# modules
import numpy as np
from random import randint, uniform
from colorsys import hsv_to_rgb
from multiprocessing import shared_memory
from random import choice, randint

class g_evolve():

    def __init__(self):
        self.number_of_workers = 10
        self.lifetime = 1
        self.reset = 1
        self.lastvalue = 0
        self.randomcolor = 0
        self.workers = []

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0

        self.safeworld = np.zeros([3, 10, 10, 10])

        for i in range(2):
            self.workers.append(worker(self.lifetime))


    def return_values(self):
        return [b'g_evolve', b'number', b'lifetime', b'', b'channel']


    def return_gui_values(self):
        if 4 > self.channel >=0:
            channel = str(self.channel)
        elif self.channel < 0:
            channel = 'noS2L'
        else:
            channel = 'Trigger'

        if self.randomcolor == 0:
            color = 'off'
        else:
            color = 'on'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.number_of_workers,2)), str(round(self.reset,2)), color, channel),'utf-8')


    def __call__(self, args):
        self.number_of_workers = int((args[0])*20)+1
        self.lifetime = int(args[1]*100+1)
        # self.randomcolor = int(round(args[2]))
        self.channel = int(args[3]*5)-1

        if self.channel == 4 :
            current_volume = int(float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                # boost one worker
                id = randint(0, len(self.workers)-1)

                self.workers[id].boost()


        world = np.zeros([3, 10, 10, 10])

        to_kill = []
        for i in range(len(self.workers)):
            world, alive = self.workers[i].run(world)

            if not alive:
                to_kill.append(i)

        to_kill.sort()
        for i in to_kill[::-1]:
            self.workers.pop(i)


        if len(self.workers) < self.number_of_workers:
            self.workers.append(worker(self.lifetime))

        return np.clip(np.round(world,2), 0, 1)


def gaussian_filter(pos, sigma=1, muu=0):

    x, y, z = np.meshgrid(np.linspace(0, 9),
                          np.linspace(0, 9),
                          np.linspace(0, 9))

    arr = np.zeros([10, 10, 10])
    for x in range(10):
        for y in range(10):
            for z in range(10):
                arr[x,y,z] = np.sqrt((x-pos[0])**2 + (y-pos[1])**2 + (z-pos[2])**2)

    #dst = np.sqrt((x-pos[0])**2 + (y-pos[1])**2 + (z-pos[2])**2)
    # dst = np.sqrt((x-pos[0])**2 + (y-pos[1])**2 + (z-pos[2])**2)

    # normalization
    normal = 1/(2.0 * np.pi * sigma**2)

    # Calculating Gaussian filter
    gauss = np.exp(-((arr)**2 / (2.0 * sigma**2))) * normal

    return gauss

class worker:
    def __init__(self,  lifetime):

        self.position  = [randint(0,9), randint(0,9), randint(0,9) ]
        self.lifetime  = lifetime
        self.starttime = lifetime

    def run(self, world):

        if self.lifetime <= 0:
            message = False
        else:
            message = True

            if self.lifetime > self.starttime/2.0:

                temp = ((self.starttime-self.lifetime)/self.starttime)*gaussian_filter(self.position, 1.1-self.lifetime/self.starttime)

                world[0, :, :, :] += temp
                world[1, :, :, :] += temp
                world[2, :, :, :] += temp

            else:

                temp = (self.lifetime/self.starttime)*gaussian_filter(self.position, 1.1-self.lifetime/self.starttime)

                world[0, :, :, :] += temp
                world[1, :, :, :] += temp
                world[2, :, :, :] += temp

            '''
            if self.lifetime > self.starttime/2.0:

                world[:, self.position[0], self.position[1], self.position[2]] = np.clip(self.lifetime / (self.starttime/2), 0, 2)
            else:

                world[0, :, :, :] += self.lifetime*gaussian_filter(self.position, 1.1-self.lifetime/self.starttime)
                world[1, :, :, :] += world[0, :, :, :]
                world[2, :, :, :] += world[0, :, :, :]
            # world[:, self.position[0], self.position[1], self.position[2]] = np.clip(self.lifetime / self.starttime, 0, 2)
            '''
            # mv = numpy.random.multivariate_normal(mean = self.position, )

        self.lifetime -= 1

        return world, message

    def boost(self):
        #print(self.lifetime, end = '->')
        self.lifetime = self.starttime
        #print(self.lifetime)
