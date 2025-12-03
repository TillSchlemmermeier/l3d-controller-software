# modules
import numpy as np
from scipy.signal import sawtooth
from generators.g_genhsphere import gen_hsphere
from multiprocessing import shared_memory
import struct

# fortran routine is in g_growing_sphere_f.f90

class g_sphere:
    '''
    Generator: growing_sphere

    a growing hollow sphere in the middle of the cube

    Parameters:
    - maxsize
    - growspeed
    - oscillate y/n
    '''

    def __init__(self):
        self.maxsize = 10
        self.growspeed = 1
        self.oscillate = 0
        self.step = 0
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0
        self.last_value = 0
        self.smooth = 0.25
        self.trigger = False
        self.sintrigger = False
        self.lastosci = 0

    #Strings for GUI
    def return_state(self):
        return [
            ['maxsize', 'maxsize', round(self.maxsize,2)],
            ['speed', 'growspeed', round(self.growspeed,2)],
            [
                'smooth' if isinstance(self.channel, int) else 'shape',
                'oscillate',
                round(self.smooth,2) if isinstance(self.channel, int) else self.oscillate
            ],
            ['channel', 'channel', self.channel],
        ]
        
    def __call__(self, args):
        # === PARAMETERS START ===
        self.maxsize = args[0]*10
        self.growspeed = args[1]
        self.oscillate = ['sin', 'explode', 'implode'][round(args[2]*2)]
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger', 'Trigger2'][int(args[3]*6)]
        # === PARAMETERS END ===

        self.smooth = args[2] / 2

        world = np.zeros([3, 10, 10, 10])

        # check if S2L is activated
        if isinstance(self.channel, int):
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
            current_volume = (1-self.smooth) * current_volume + self.smooth * self.last_value

            if self.growspeed < 1.0:
                if current_volume < self.last_value:
                    current_volume = self.last_value-self.growspeed**2

            current_volume = np.clip(current_volume,0,1)
            self.last_value = current_volume

            size = self.maxsize*current_volume


        #check for trigger
        elif self.channel in ['Trigger', 'Trigger2']:
            if self.channel == 'Trigger':
                current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            else:
                current_volume = struct.unpack('d', bytes(self.sound_values.buf[40:48]))[0]

            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.step = 0
                self.trigger = False
                self.sintrigger = False
                self.lastosci = 0

            # oscillates between 0 and 1
            if self.oscillate == 'sin':
                if self.sintrigger:
                    osci = 0
                else:
                    osci = np.sin(self.step*self.growspeed)*0.5 + 0.5
                    if osci < self.lastosci:
                        self.trigger = True
                    if self.trigger:
                        if osci > self.lastosci:
                            self.sintrigger = True

            elif self.oscillate == 'implode':
                if self.trigger:
                    osci = 0
                else:
                    osci = sawtooth(self.step*self.growspeed, 0)*0.5 + 0.5
                    if osci > self.lastosci:
                        self.trigger = True

            else:
                if self.trigger:
                    osci = 0
                else:
                    osci = sawtooth(self.step*self.growspeed)*0.5 + 0.5
                    if osci < self.lastosci:
                        self.trigger = True

            # scales to maxsize
            size = self.maxsize * osci
            self.lastosci = osci
            self.step += 1


        else:
            # oscillates between 0 and 1
            if self.oscillate == 'sin':
                osci = np.sin(self.step*self.growspeed)*0.5 + 0.5
            elif self.oscillate == 'implode':
                osci = sawtooth(self.step*self.growspeed, 0)*0.5 + 0.5
            else:
                osci = sawtooth(self.step*self.growspeed)*0.5 + 0.5

            # scales to maxsize
            size = self.maxsize * osci
            self.step += 1

        # creates hollow sphere with parameters
        world[0, :, :, :] = gen_hsphere(size, 4.5, 4.5, 4.5)
        world[1:, :, :, :] = world[0, :, :, :]
        world[2:, :, :, :] = world[0, :, :, :]

        return np.round(np.clip(world, 0, 1), 3)
