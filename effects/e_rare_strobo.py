# modules
import numpy as np
from random import random, choice

class e_rare_strobo():
    '''
    Effect: rare strobo

    blend in channel with strobo after some
    waiting time.
    additionally, displace the figure randomly by some Probabilty
    '''

    def __init__(self):
        self.waiting_frames = 100
        self.strobo_frames = 10
        self.disp_prop = 0
        self.counter = 0
        self.state = 'wait'
        self.step = 0

    def control(self, waiting_frames, strobo_frames, disp_prop):
        self.waiting_frames = int(waiting_frames*300)+50
        self.strobo_frames = int(strobo_frames*20)+2
        self.disp_prop = disp_prop*0.5

    #strings for GUI
    def return_values(self):
        return [b'rare_strobo', b'Waiting Frames', b'Strobo Frames', b'Displacement Probability', b'']

    def generate(self, step, world):

        if self.state == 'wait':
            # waiting part
            self.counter += 1
            if self.counter > self.waiting_frames:
                self.state = 'strobo'
                self.counter = 0

            world *= 0

        elif self.state == 'strobo':
            # strobo part
            world[:, :, :, :] *= self.step % 2
            self.counter += 1


            # and do some displacement
            if random() < self.disp_prop:
                shift = choice([-1,1])
                ax = choice([0,1,2])
                world[0, :, :, :] = np.roll(world[0, :, :, :], axis = ax, shift=shift)
                world[1, :, :, :] = np.roll(world[1, :, :, :], axis = ax, shift=shift)
                world[2, :, :, :] = np.roll(world[2, :, :, :], axis = ax, shift=shift)


            if self.counter > self.strobo_frames:
                self.state = 'wait'

            self.step +=1

        return np.clip(world, 0, 1)
