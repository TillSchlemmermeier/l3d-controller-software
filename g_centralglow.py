# modules
import numpy as np


class g_centralglow():
    '''
    Generator: centralglow

    glows up the inside of the cube. There are two counters: One for the
    brigthness, one for the waiting time.
    If brigthness exceeds 1, the waiting counter starts to count down to zero
    and the brightness is set to 0.0.
    When zero is reached, the brightness counter starts to build up again.

    Parameters:
    - speed
    - wainting time
    '''

    def __init__(self):
        self.speed = 0.1
        self.waiting = 10

        self.brigthness = 0.0
        self.waitingcounter = 0


    def control(self, speed, waiting, dump):
        self.speed = speed
        self.waiting = int(waiting*50)

    def label(self):
        return ['speed',self.speed,'waiting', self.waiting,'empty','empty']


    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

        if self.brightness > 1.0
            self.waitingcounter = self.waiting
            self.speedcounter = 0.0

        elif self.waitingcounter == 0:
            for x in range(10):
                for y in range(10):
                    for z in range(10):
                        world[:, x, y, z] = self.brightness * (1.0/((np.sqrt((4.5-x)**2 + (4.5-y)**2 + (4.5-z)**2)))**1)
            self.brightness += self.speed

        else:
            self.waitingcounter -= 1:

        return np.clip(world, 0, 1)
