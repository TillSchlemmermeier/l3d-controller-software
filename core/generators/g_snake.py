import struct
import numpy as np
from random import randint, random, choice
from multiprocessing import shared_memory

# the 26 neighbours of a voxel
NEIGHBOURS = np.array([(x, y, z) for x in (-1, 0, 1) for y in (-1, 0, 1) for z in (-1, 0, 1) if (x, y, z) != (0, 0, 0)])

class g_snake():
    '''
    Generator: a head walks through the cube and leaves a fading body.

    snake: straight along an axis, turning now and then
    grow:  to a random free neighbour that isn't crowded, so it spreads like a
           plant. A turn starts a new branch from a random point of the body
    '''

    def __init__(self):
        self.mode = 'snake'
        self.turn = 0.25
        self.length = 1
        self.channel = 'noS2L'

        self.body = np.zeros([10, 10, 10])
        self.head = np.array([4, 4, 4])
        self.direction = np.array([1, 0, 0])

        self.sound_values = shared_memory.SharedMemory(name="global_s2l_memory")
        self.lastvalue = 0

    def return_state(self):
        return [
            ['mode', 'mode', self.mode],
            ['turn', 'turn', round(self.turn, 2)],
            ['length', 'length', self.length],
            ['channel', 'channel', self.channel],
        ]

    def change_course(self):
        if self.mode == 'snake':
            # along one of the two other axes, either way
            axis = choice(np.flatnonzero(self.direction == 0))
            self.direction = np.zeros(3, dtype=int)
            self.direction[axis] = choice([-1, 1])
        else:
            lit = np.argwhere(self.body > 0)
            if len(lit):
                self.head = lit[randint(0, len(lit) - 1)]

    def move(self):
        if self.mode == 'snake':
            self.head = (self.head + self.direction) % 10
            return

        for _ in range(20):
            probe = (self.head + NEIGHBOURS[randint(0, 25)]) % 10
            # free, and next to the head and at most one other lit voxel
            crowd = np.count_nonzero(self.body[tuple(((probe + NEIGHBOURS) % 10).T)])
            if self.body[tuple(probe)] == 0 and crowd <= 2:
                self.head = probe
                return
        # stuck in its own body
        self.change_course()

    def __call__(self, args):
        # === PARAMETERS START ===
        self.mode = ['snake', 'grow'][int(args[0] > 0)]
        self.turn = args[1]
        self.length = round(args[2]*99) + 1
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][int(args[3]*5)]
        # === PARAMETERS END ===

        # the body fades out over `length` frames
        self.body = np.maximum(self.body - 1/self.length, 0)

        steps, turn = 1, self.turn
        # turns on the beat only
        if self.channel == 'Trigger':
            beats = struct.unpack('d', self.sound_values.buf[32:40])[0]
            turn = float(beats > self.lastvalue)
            self.lastvalue = beats
        # the louder the band, the faster it moves. Silence stands still
        elif self.channel != 'noS2L':
            volume = struct.unpack('d', self.sound_values.buf[self.channel*8:self.channel*8+8])[0]
            steps = round(min(volume, 1)*3)

        for _ in range(steps):
            if random() < turn:
                self.change_course()
            self.move()
            self.body[tuple(self.head)] = 1

        return np.stack([self.body]*3)
