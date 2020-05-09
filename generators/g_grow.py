# modules
import numpy as np
from random import randint, random
from time import sleep

class g_grow():

    def __init__(self):
        self.branch = 0
        self.probecolor = 1
        self.age = 0.02
        self.active = [randint(0, 9), randint(0, 9), randint(0, 9)]

        self.world = np.zeros([3, 10, 10, 10])
        self.state = 'grow'

        self.probes = []

    def return_values(self):
        return [['', ''],
				['', ''],
				['', '']]

    def __call__(self, args):
        # parse arguments
        self.branch = args[0]*0.5
        self.probecolor = int(args[1]+0.5)
        self.age = args[2]*0.1

        # age world
        self.world = np.clip(self.world - self.age, 0, 1)

        # check and grow
        if self.state == 'grow':
            # grow active point
            self.world[:, self.active[0], self.active[1], self.active[2]] = 1
            self.state = 'explore'

        # explore
        elif self.state == 'explore':
            breakcounter = 0
            while True:
                # check for infinity loop
                if breakcounter > 20:
                    print('growing stuck!')
                else:
                    breakcounter += 1

                # create probe
                self.probe = [self.active[0]+randint(-1,1), self.active[1]+randint(-1,1), self.active[2]+randint(-1,1)]

                # check for boundaries
                for i in range(3):
                    if self.probe[i] == 10:
                        self.probe[i] = 0
                    elif self.probe[i] == -1:
                        self.probe[i] = 9

                # check that the place is free
                if self.world[0, self.probe[0], self.probe[1], self.probe[2]] == 0:
                    if self.probecolor == 1:
                        color = [1.0, 0, 0]
                    else:
                        color = [0.5, 0.5, 0.5]

                    for c,i in zip(color, range(3)):
                        self.world[i, self.probe[0], self.probe[1], self.probe[2]] = c

                    self.state = 'check'
                    break

        # check whether exploring was succesful
        elif self.state == 'check':
            # count neighbours
            n_neighbours = 0
            for x in [-1, 0, 1]:
                temp = np.roll(self.world[1, :, :, :], x, axis = 0)
                for y in [-1, 0, 1]:
                    n_neighbours += np.roll(temp, y, axis = 1)[self.probe[0], self.probe[1], self.probe[2]]

                # substract probe from neighbours
                n_neighbours -= 0.5

                # if less than 3 neighbours, add to active
                if n_neighbours <= 2:
                    self.active = self.probe
                    self.state = 'grow'
                # else delete probe and go back to explore
                else:
                    self.state = 'explore'
                    self.world[:, self.probe[0], self.probe[1], self.probe[2]] = 0.0

        else:
            print('unkown state!')
            self.state = 'grow'

        return np.clip(self.world, 0, 1)
