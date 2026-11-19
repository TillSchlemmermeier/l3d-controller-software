# modules
import struct
import numpy as np
from random import randint, random
from multiprocessing import shared_memory

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

    def __init__(self):
        self.speed = 1
        self.drops = []
        self.step = 1
        self.drops.append(self.drop())
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 'noS2L'
        self.lastvalue = 0

    def return_state(self):
        return [
            ['speed', 'speed', round(self.speed,2)],
            ['channel', 'channel', self.channel],
        ]

    def __call__(self, args):
        # === PARAMETERS START ===
        self.speed = 12-int(args[0]*10 + 1)
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][int(args[1]*5)]
        # === PARAMETERS END ===

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

        if self.channel == 'noS2L':
            new_drops = int(self.step % self.speed == 0)

        # a burst on each beat, the bigger the faster
        elif self.channel == 'Trigger':
            beats = struct.unpack('d', self.sound_values.buf[32:40])[0]
            new_drops = 12 - self.speed if beats > self.lastvalue else 0
            self.lastvalue = beats

        # the louder the band, the denser the rain. At full volume as dense as the timer
        else:
            volume = struct.unpack('d', self.sound_values.buf[self.channel*8:self.channel*8+8])[0]
            new_drops = int(random() < min(volume, 1)/self.speed)

        self.drops += [self.drop() for _ in range(new_drops)]
        self.step += 1

        return np.clip(world, 0, 1)
