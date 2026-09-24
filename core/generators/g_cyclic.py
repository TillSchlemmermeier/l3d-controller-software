# modules
import struct
import numpy as np
from multiprocessing import shared_memory


class g_cyclic():
    '''
    Generator: cyclic

    A cyclic cellular automaton. Every voxel holds a phase and may only step
    forward to the next one if a neighbour is already there, so the whole cube
    organises itself into rolling spiral waves that chase each other and never
    settle down.

    Parameters:
    - length : length of the phase cycle, decides how wide the waves are
    - speed  : 1 crawls, 6 steps the automaton on every frame
    - smooth : eases the brightness between steps, from strobing to flowing
    - s2l channel
    '''

    # slowest setting, in frames between two automaton steps. anything past
    # this just reads as a lagging animation rather than a slow one
    SLOWEST = 6

    def __init__(self):
        self.length = 10
        self.speed = 3
        self.smooth = 0.4
        self.step = 0
        self.stuck = 0
        self.state = np.random.randint(0, self.length, [10, 10, 10]).astype(np.int8)
        self.bright = np.zeros([10, 10, 10])
        # s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0

    def return_state(self):
        return [
            ['length', 'length', self.length],
            ['speed', 'speed', self.speed],
            ['smooth', 'smooth', round(self.smooth,2)],
            ['channel', 'channel', self.channel],
        ]

    def seed(self):
        '''throw random phases back into the cube, every phase gets used'''
        self.stuck = 0
        self.state = np.random.randint(0, self.length, [10, 10, 10]).astype(np.int8)

    def advance(self):
        '''a voxel may only move on if a neighbour already holds the next phase'''
        nxt = (self.state + 1) % self.length
        neighbours = ((np.roll(self.state, 1, 0) == nxt).astype(np.int8)
                    + (np.roll(self.state, -1, 0) == nxt)
                    + (np.roll(self.state, 1, 1) == nxt)
                    + (np.roll(self.state, -1, 1) == nxt)
                    + (np.roll(self.state, 1, 2) == nxt)
                    + (np.roll(self.state, -1, 2) == nxt))

        moved = np.where(neighbours > 0, nxt, self.state)

        # if a phase is missing from the cube nobody can step over the gap and
        # the automaton is deadlocked for good, so start it over
        if np.array_equal(moved, self.state):
            self.stuck += 1
            if self.stuck > 2:
                self.seed()
        else:
            self.stuck = 0
            self.state = moved

    def __call__(self, args):
        previous = self.length
        # === PARAMETERS START ===
        self.length = int(args[0]*8)+6
        self.speed = int(args[1]*5)+1
        self.smooth = args[2]*0.8+0.15
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][int(args[3]*5)]
        # === PARAMETERS END ===

        # the cycle length changed. reseed rather than rescale, every phase has
        # to be present somewhere or the waves cannot travel round the cycle
        if self.length != previous:
            self.seed()

        # the knob reads as a speed, the automaton wants a gap between steps,
        # so a high speed has to become a short gap
        interval = self.SLOWEST - self.speed + 1

        # check if S2L is activated
        if isinstance(self.channel, int):
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
            # loud parts drive the waves faster, up to a step on every frame.
            # a band over 1 just pins it there, which is the right end to stick
            interval = max(1, int(round(interval * (1 - current_volume))))

        #check for trigger
        elif self.channel == 'Trigger':
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            if current_volume > self.lastvalue:
                self.seed()
            self.lastvalue = current_volume

        if self.step % interval == 0:
            self.advance()

        # a narrow lobe around phase zero, so only the wave fronts light up
        target = np.clip(np.cos(2*np.pi*self.state/self.length), 0, 1)**2
        self.bright += (target - self.bright) * self.smooth

        self.step += 1

        # transfer to real world
        world = np.zeros([3, 10, 10, 10])
        for i in range(3):
            world[i, :, :, :] = self.bright

        return np.clip(world, 0, 1)
