# modules
import struct
import numpy as np
from multiprocessing import shared_memory


class g_voronoi():
    '''
    Generator: voronoi

    A handful of seed points drift through the cube and every voxel belongs to
    whichever seed is nearest. Lighting only the boundaries leaves a shifting
    honeycomb of crystal facets, filling the cells instead gives slabs of light
    sliding past each other. Nothing else here partitions the volume.

    Parameters:
    - number : how many cells the cube is broken into
    - width  : thickness of the walls between them
    - speed  : how fast the seeds wander
    - s2l channel
    '''

    MAX_SEEDS = 10
    # thinnest the walls are ever drawn, the bottom of the width knob's own range
    WIDTH_MIN = 0.25
    # a beat swells the walls by this much on top of whatever the knob asks for,
    # then they shrink back. it rides above the knob rather than scaling it, so
    # the pulse is still there with the walls already set fat
    KICK_SWELL = 0.9
    KICK_DECAY = 0.85

    def __init__(self):
        self.number = 6
        self.width = 0.8
        self.speed = 0.05
        self.kick = 0.0

        self.points = np.random.uniform(0, 9, [self.MAX_SEEDS, 3])
        self.velocity = np.random.uniform(-1, 1, [self.MAX_SEEDS, 3])
        self.velocity /= np.linalg.norm(self.velocity, axis=1, keepdims=True)

        # voxel coordinates, built once
        axis = np.arange(10.0)
        self.gx, self.gy, self.gz = np.meshgrid(axis, axis, axis, indexing='ij')

        # s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0

    def return_state(self):
        return [
            ['number', 'number', self.number],
            ['speed', 'speed', round(self.speed,3)],
            ['width', 'width', round(self.width,2)],
            ['channel', 'channel', self.channel],
        ]

    def __call__(self, args):
        # === PARAMETERS START ===
        self.number = int(args[0]*(self.MAX_SEEDS-3))+3
        self.speed = args[1]*0.25+0.01
        self.width = args[2]*0.85+0.25
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][int(args[3]*5)]
        # === PARAMETERS END ===

        width = self.width

        # check if S2L is activated
        if isinstance(self.channel, int):
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
            # the walls swell with the sound, so the crystal thickens on a hit.
            # thickness is the one control here that moves how much of the cube
            # is lit, and on ten voxels that is what reads
            width = self.WIDTH_MIN + min(current_volume, 1.0)*(self.width - self.WIDTH_MIN)

        #check for trigger
        elif self.channel == 'Trigger':
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            self.kick *= self.KICK_DECAY      # decay first, so a beat lands at full strength
            if current_volume > self.lastvalue:
                self.kick = 1.0
            self.lastvalue = current_volume
            # the honeycomb flares on the beat and thins out again
            width = self.width + self.kick*self.KICK_SWELL

        # drift the seeds and bounce them off the walls
        self.points += self.velocity * self.speed
        outside = (self.points < 0) | (self.points > 9)
        self.velocity[outside] *= -1
        np.clip(self.points, 0, 9, out=self.points)

        active = self.points[:self.number]

        # distance from every voxel to every seed
        distances = np.sqrt((self.gx - active[:, 0].reshape(-1, 1, 1, 1))**2
                          + (self.gy - active[:, 1].reshape(-1, 1, 1, 1))**2
                          + (self.gz - active[:, 2].reshape(-1, 1, 1, 1))**2)

        # a wall is where the two closest seeds are almost equally far away
        nearest_two = np.partition(distances, 1, axis=0)[:2]
        gap = nearest_two[1] - nearest_two[0]

        field = np.clip(1 - gap/width, 0, 1)

        # transfer to real world
        world = np.zeros([3, 10, 10, 10])
        for i in range(3):
            world[i, :, :, :] = field

        return np.clip(world, 0, 1)
