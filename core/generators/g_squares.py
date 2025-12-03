import struct
import numpy as np
from scipy.signal import sawtooth
from multiprocessing import shared_memory

class g_squares():
    '''
    Generator: squares
    a square moving up and down the edges

    Parameters:
    speed
    direction (x, y or z)
    type (sinus, up or down)
    Sound2Light trigger On / Off
    '''

    def __init__(self):
        self.speed = 10
        self.dir = 'X'
        self.type = 0
        self.step = 0
        self.pause = 0
        self.squares = [0]

        # s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.trigger = False
        self.lastvalue = 0
        self.nextposition = 0
        self.switch = False
        self.stop = False

    def return_state(self):
        return [
            ['speed', 'speed', round(self.speed,2)],
            ['dir', 'dir', self.dir],
            ['type', 'type', self.type],
            ['Trigger', 'trigger', 'On' if self.trigger else 'Off'],
            ['pause', 'pause', round(self.pause, 2)],
        ]
    
    def __call__(self, args):
        # === PARAMETERS START ===
        self.speed = int(args[0]*8) + 1
        self.dir = ['X', 'Y', 'Z'][int(round(args[1]*2))]
        self.type = ['cos', 'up', 'down'][int(round(args[2]*2))]
        self.trigger = args[3] >= 0.5
        self.pause = int(round((args[4]* 30) + 1))
        # === PARAMETERS END ===

        world = np.zeros([3, 10, 10, 10])

        #check for trigger
        if self.trigger:
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.step = 0
                self.switch = False
                self.stop = False
                if self.type == 'cos' or self.type == 'up':
                    self.nextposition = 0
                else:
                    self.nextposition = 9

            position = self.nextposition
            self.squares = []
            self.squares.append(position)

            if not self.stop:
                if self.type == 'cos':
                    nextposition = 9-int(round((np.cos(0.1*(self.step+1)*self.speed)+1)*4.5))
                    if nextposition < position:
                        self.switch = True

                    if self.switch:
                        if nextposition > position:
                            self.stop = True

                elif self.type == 'up':
                    nextposition = int(round((sawtooth(0.1*(self.step+1)*self.speed)+1)*4.5))
                    if nextposition < position:
                        self.stop = True

                else:
                    nextposition = int(round((sawtooth(0.1*(self.step+1)*self.speed, width=0)+1)*4.5))
                    if nextposition > position:
                        self.stop = True

                if not self.stop:
                    self.step += 1
                    self.nextposition = nextposition

        else:
            if self.type == 'cos':
                active_squares = []
                for pos in self.squares:
                    # only one square at a time for cos
                    pos = 9-int(round((np.cos(0.1*self.step*self.speed)+1)*4.5))
                    active_squares.append(pos)
                    self.squares = active_squares

            else:
                if self.step % (self.pause * (10 - self.speed)) == 0:
                    if self.type == 'up':
                        self.squares.append(0)
                    else:
                        self.squares.append(9)

                if self.step % (10 - self.speed) == 0:
                    active_squares = []
                    for pos in self.squares:
                        if self.type == 'up':
                            pos += 1
                        else:
                            pos -= 1

                        if 0 <= pos <= 9:
                            active_squares.append(pos)
                    self.squares = active_squares

        for pos in self.squares:
            if self.dir == 'X':
                world[:, pos, :, :] = 1.0
                world[:, :, 1:-1, 1:-1] = 0.0
            elif self.dir == 'Y':
                world[:, :, pos, :] = 1.0
                world[:, 1:-1, :, 1:-1] = 0.0
            else:
                world[:, :, :, pos] = 1.0
                world[:, 1:-1, 1:-1, :] = 0.0

        self.step += 1

        return world
