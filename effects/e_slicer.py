
import numpy as np
from multiprocessing import shared_memory
from random import randint

class e_slicer():


    def __init__(self):
        # parameters
        self.slices = []
        self.number = 5
        for i in range(self.number):
            self.slices.append(randint(0, 9))

        self.channel = 1.0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

        self.counter = 1

    def return_values(self):
        # strings for GUI
        return [b'slicer', b'number', b'channel', b'n frames', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.number,0)), str(self.channel), str(self.frames),'') ,'utf-8')

    def __call__(self, world, args):
        # process parameters
        # self.amount = args[0]*2
        self.number = int(args[0]*3)+3
        self.channel = int(round(args[1]*3))
        self.frames = int(args[2]*10+5)

        current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
        current_volume = np.clip(current_volume, 0, 1)

        brightness = [0 for x in range(10)]

        for i in range(len(self.slices)):
            brightness[self.slices[i]] = current_volume
            current_volume -= 0.1
            current_volume = np.clip(current_volume, 0, 4)

        for i in range(len(brightness)):
            world[:, i, :, :] *= brightness[i]

        self.counter += 1

        if self.counter > self.frames:
            self.counter = 0
            self.slices = []
            for i in range(self.number):
                self.slices.append(randint(0, 9))


        return np.clip(world, 0, 1)
