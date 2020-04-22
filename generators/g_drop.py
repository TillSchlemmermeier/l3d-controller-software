# modules
import numpy as np
from random import randint

class g_drop():

    class drop():

        def __init__(self):
            self.x = 0
            self.y = randint(0,9)
            self.z = randint(0,9)

            self.brightness = 0.0

            self.state = 0

        def do_step(self):

            temp = [self.x, self.y, self.z, self.brightness, self.state]

            # do stuff
            if self.state == 0:
                self.brightness += 0.1

            elif self.state == 1:
                self.x += 1

            elif self.state == 2:
                self.brightness -= 0.1

            # update state
            if self.brightness >= 1.0 and self.state == 0:
                self.state = 1

            elif self.x >= 9 and self.state != 2:
                self.state = 2

            elif self.brightness <= 0.0 and self.state == 2:
                self.state = 3

            return temp

    '''
    Generator: drop
    '''

    def __init__(self):
        self.speed = 1
        self.drops = []
        self.drops.append(self.drop())

    def return_values(self):
        pass

    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.speed = int(args[0]*10 + 1)

        # create world
        world = np.zeros([3, 10, 10, 10])

        n_del = 0

        # do step
        for i in range(len(self.drops)):
            [x, y, z, b, s] = self.drops[i-n_del].do_step()
            world[:, x, y, z] = b
            if s == 3:
                del(self.drops[i-n_del])
                n_del += 1

        if step%self.speed == 0:
            self.drops.append(self.drop())

        return np.clip(world, 0, 1)
