# modules
import struct
import numpy as np
from random import randint
from multiprocessing import shared_memory

class g_evolve():

    def __init__(self):
        self.number_of_workers = 10
        self.lifetime = 1
        self.lastvalue = 0
        self.width = 1
        self.workers = []

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.trigger = False

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

        if self.trigger:

            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
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


# the x, y and z of every voxel
GRID = np.indices((10, 10, 10))

def gaussian_filter(pos, sigma=1):
    # squared distance of every voxel to pos
    distance2 = np.sum((GRID - np.reshape(pos, (3, 1, 1, 1)))**2, axis=0)
    return np.exp(-distance2/(2.0*sigma**2))

class worker:
    def __init__(self,  lifetime, width):

        self.width = width
        self.position  = [randint(0,9), randint(0,9), randint(0,9) ]
        self.lifetime  = lifetime + randint(-3, 3)
        self.starttime = self.lifetime

        self.wait = 0

    def run(self, world):
        alive = self.lifetime > 0
        if alive:
            # brightens to full at half its life and back to 0, while it keeps growing
            brightness = 2*min(self.starttime - self.lifetime, self.lifetime)/self.starttime
            sigma = (self.width + 0.01) - self.width*self.lifetime/self.starttime
            # a boost doubles it on the beat, fading out over 10 frames
            world += brightness**2*gaussian_filter(self.position, sigma)*(1 + self.wait/10)

        # a boosted worker pauses its life while the boost lasts
        if self.wait > 0:
            self.wait -= 1
        else:
            self.lifetime -= 1

        return world, alive

    def boost(self):
        self.wait = 10
