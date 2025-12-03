import numpy as np
from random import randint

class g_full_drip():

    def __init__(self):
        self.drops = []
        self.n = 10
        self.stop_pos = 9

        for i in range(50):
            self.drops.append(led())

    def return_state(self):
            return [
            ['number', 'n', self.n],
            ['stop pos', 'stop_pos', self.stop_pos],
        ]


    def __call__(self, args):
        # === PARAMETERS START ===
        self.n = int(args[0]*40)+1
        self.stop_pos = int(round(args[1]*10,0))
        # === PARAMETERS END ===

        world = np.zeros([3, 10, 10, 10])

        for i in range(self.n):
            temp = self.drops[i].run(self.drops)
            if len(temp) == 3:
                world[:, temp[0], temp[1], temp[2]] = 1.0
            else:
                self.drops[i] = led(self.stop_pos)

        return np.clip(world, 0, 1)**2


class led:
    def __init__(self, stop_pos = 9):
        self.x, self.y, self.z = 0, randint(0,9), randint(0,9)
        self.stop_x = np.clip(stop_pos + randint(0, 1),0,9)
        if stop_pos >= 9:
            self.stop_x = 9
        self.stop_t = randint(10, 40)
        self.state = 'run'


    def run(self, leds):

        # perform action
        if self.state == 'run':
            output = [self.x, self.y, self.z]
            # check for collisions:
            # ind = np.where(self.y == np.array([l.x for l in leds]))[0]
            self.x += 1
        elif self.state == 'wait':
            output = [self.x, self.y, self.z]
            self.stop_t -= 1
        elif self.state == 'dead':
            output = [0]

        # update state
        if self.x > 9 or self.state == 'dead':
            self.state = 'dead'
        else:
            if self.x == self.stop_x and self.state == 'run':
                self.state = 'wait'
            elif self.state == 'wait' and self.stop_t <= 0:
                self.state == 'run'
                self.x += 1

        return np.clip(output,0,9)
