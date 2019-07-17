# modules
import numpy as np
from random import randint, choice
from copy import deepcopy

class g_collision():
    def __init__(self):
        self.assign_beams()

        # 0 for incoming beam, 1 for outgoing beam, 2 for reset
        self.state = 0

    def control(self, blub0, blub1, blub2):
        pass

    def label(self):
        return ['empty', 'empty',
                'empty', 'empty',
                'empty', 'empty',]

    def generate(self, step, world):
        world = np.zeros([3, 10, 10, 10])

        if self.state == 0:
            coords = self.beam_in()
            if coords is not None:
                world[:, coords[0], coords[1], coords[2]] = 1.0
            else:
                self.state += 1

            # print(0, coords)

        elif self.state == 1:
            coords1 = self.beam_out1()
            coords2 = self.beam_out2()

            if coords1 is not None and coords2 is not None:
                world[:, coords1[0], coords1[1], coords1[2]] = 1.0
                world[:, coords2[0], coords2[1], coords2[2]] = 1.0
            elif coords1 is not None and coords2 is None:
                world[:, coords1[0], coords1[1], coords1[2]] = 1.0
            elif coords1 is None and coords2 is not None:
                world[:, coords2[0], coords2[1], coords2[2]] = 1.0
            else:
                self.state += 1

            # print(1, coords1, coords2)

        elif self.state == 2:
            self.assign_beams()
            self.state = 0

        # print(self.state)

        return np.clip(world, 0, 1)

    def assign_beams(self):
        axis = randint(0,2)
        p2 = [randint(1,8), randint(1,8), randint(1,8)]

        p1 = deepcopy(p2)
        p1[axis] = choice([0,9])

        p1_1 = deepcopy(p2)
        p1_2 = deepcopy(p2)

        if axis == 0:
            p1_1[1] = choice([0, 9])
            p1_2[2] = choice([0, 9])
        elif axis == 1:
            p1_1[0] = choice([0, 9])
            p1_2[2] = choice([0, 9])
        else:
            p1_1[0] = choice([0, 9])
            p1_2[1] = choice([0, 9])

        # print(p1, p2, p1_1, p1_2)

        self.beam_in = beam(p1, p2)
        self.beam_out1 = beam(p2, p1_1)
        self.beam_out2 = beam(p2, p1_2)

class beam:
    def __init__(self, p1, p2):
        # p1 is outside, p2 is inside
        self.p1 = np.array(p1)
        self.p2 = np.array(p2)
        # calculate vector
        self.vec = self.p2-self.p1
        # calculate "length" of vector
        self.steps = np.abs(np.cumsum(self.vec)[-1])
        self.counter = -1

    def __call__(self):
        if self.counter < self.steps:
            # return point
            self.counter += 1
            return np.array(self.p1 + self.counter * (self.vec/self.steps), dtype = int)

        else:
            # return none
            return None
