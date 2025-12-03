import numpy as np
from random import randint

class g_stacking():

    def __init__(self):
        self.drops = []
        self.n = 10
        self.channel = 0
        self.lifetime = 2

        for i in range(220):
            self.drops.append(led(10))

    def return_state(self):
        return [
            ['number', 'n', self.n],
            ['lifetime', 'lifetime', self.lifetime],
        ]
    
    def __call__(self, args):
        # === PARAMETERS START ===
        self.n = int(args[0]*200)+1
        self.lifetime = int(args[1]*50) + 5
        # === PARAMETERS END ===

        world = np.zeros([3, 10, 10, 10])
        # append new leds at top
        # for i in range(self.n):
        #     self.drops.append(led(9))

        # check for dead leds
        for i in range(self.n):
            self.drops[i].stop_t = self.lifetime
            temp = self.drops[i].run(self.drops[:self.n])
            # print(self.drops[i].state)

            if len(temp) == 3:
                world[:, temp[0], temp[1], temp[2]] = 1.0
            else:
                self.drops[i] = led(self.lifetime)

        # print(' ')
        return np.clip(world, 0, 1)**2


class led:
    def __init__(self, waittime):
        self.x, self.y, self.z = 0, randint(0,9), randint(0,9)
#        self.x, self.y, self.z = 0, 0, 0
        self.stop_x = 9
        self.stop_t = waittime
        self.current_t = waittime
        self.state = 'run'


    def run(self, leds):

        # perform action
        if self.state == 'run':
            output = [self.x, self.y, self.z]
            # check for collisions:
            run = True
            for led in leds:
                if led.z == self.z and led.y == self.y:
                    # print(led.x, self.x)
                    if led.x == self.x+1: #  and led.state == 'wait':
                        run = False
                        # print('dont run')

            if run:
                self.x += 1
        elif self.state == 'wait':
            output = [self.x, self.y, self.z]
            self.current_t -= 1
        elif self.state == 'dead':
            output = [0]

        if self.current_t > self.stop_t:
            self.current_t = self.stop_t

        # update state
        if self.x > 9 or self.state == 'dead':
            self.state = 'dead'
        else:
            if self.x == self.stop_x and self.state == 'run':
                self.state = 'wait'
            elif self.state == 'wait' and self.current_t <= 0:
                self.state == 'run'
                self.x += 1

        return np.clip(output,0,9)
