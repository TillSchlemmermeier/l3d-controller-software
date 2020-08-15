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

    #strings for GUI
    def return_values(self):
        return [b'rare_strobo', b'Wait #', b'Strobo #', b'Move Prob', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(waiting_frames), str(strobo_frames), str(round(self.disp_prop,1)), ''), 'utf-8')


    def __call__(self, world, args):
        # parsing input
        self.waiting_frames = int(args[0]*300)+50
        self.strobo_frames = int(args[1]*20)+2
        self.disp_prop = args[2]*0.5

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
