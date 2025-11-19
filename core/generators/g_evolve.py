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
        self.width = 1
        self.workers = []

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.trigger = False

        self.safeworld = np.zeros([3, 10, 10, 10])

        for i in range(2):
            self.workers.append(worker(self.lifetime, self.width))

    def return_state(self):
        return [
            ['number', 'number_of_workers', round(self.number_of_workers,2)],
            ['lifetime', 'lifetime', round(self.lifetime,2)],
            ['width', 'width', round(self.width,2)],
            ['trigger', 'trigger', 'On' if self.trigger else 'Off'],
        ]
    

    def __call__(self, args):
        # === PARAMETERS START ===
        self.number_of_workers = int((args[0])*20)+1
        self.lifetime = int(args[1]*100+1)
        self.width = args[2]+1
        self.trigger = args[3] > 0.5
        # === PARAMETERS END ===

        # self.randomcolor = int(round(args[2]))

        if self.trigger:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
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
            self.workers.append(worker(self.lifetime, self.width))

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
    # normal = 1/(2.0 * np.pi * sigma**2)

    # Calculating Gaussian filter
    gauss = np.exp(-((arr)**2 / (2.0 * sigma**2))) # * normal

    return gauss

class worker:
    def __init__(self,  lifetime, width):

        self.width = width
        self.position  = [randint(0,9), randint(0,9), randint(0,9) ]
        self.lifetime  = lifetime + randint(-3, 3)
        self.starttime = self.lifetime

        self.wait = 0

    def run(self, world):

        if self.lifetime <= 0:
            message = False
        else:
            message = True

            if self.lifetime > 0.5*self.starttime:
                # starting
                brightness = round(2 * (self.starttime-self.lifetime)/self.starttime,4)
                gauss      = gaussian_filter(self.position, (self.width+0.01)-self.width*self.lifetime/self.starttime)
                # temp       = brightness*
                temp = brightness**2 * gauss #* (1/np.max(gauss))

                world[0, :, :, :] += temp
                world[1, :, :, :] += temp
                world[2, :, :, :] += temp

            else:
                # ending
                brightness = 2*(self.lifetime/self.starttime)
                temp = brightness**2*gaussian_filter(self.position, (self.width+0.01)-self.width*self.lifetime/self.starttime)

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

        if self.wait > 0:
            self.wait -= 1
        else:
            self.lifetime -= 1

        return world*np.cos(self.wait * 0.1), message

    def boost(self):
        # self.lifetime = self.starttime
        self.wait = 10
