# modules
import struct
import numpy as np
from scipy.ndimage import map_coordinates
from multiprocessing import shared_memory


class g_smoke():
    '''
    Generator: smoke

    Coherent volumetric noise. Three octaves of a smooth random lattice are
    stacked on top of each other and drift through the cube, which gives
    billowing clouds and nebula rather than the uncorrelated per LED flicker
    of g_random. In terrain mode the same field is read as a height map, so
    rolling hills sweep through the volume instead.

    Parameters:
    - scale : size of the billows, small is wispy and large is one slow swell
    - mode  : cloud fills the volume, terrain draws a rolling surface
    - speed : how fast the field moves through the cube
    - s2l channel
    '''

    # a lattice this size wraps rarely enough that the drift never looks looped
    LATTICE = 16
    # relative size and weight of each octave
    OCTAVES = [(1.0, 1.0), (0.5, 0.5), (0.25, 0.25)]
    # the crawl the sound falls back to. never zero, a field standing perfectly
    # still reads as a frozen picture rather than as a quiet one
    SPEED_MIN = 0.01

    def __init__(self):
        self.scale = 5.0
        self.mode = 'cloud'
        self.speed = 0.05
        self.offset = np.zeros(3)

        # one lattice per octave, each drifting its own way so the sum has a
        # much longer period than any single one of them
        self.lattices = [np.random.rand(self.LATTICE, self.LATTICE, self.LATTICE)
                         for _ in self.OCTAVES]
        self.headings = [np.random.uniform(-1, 1, 3) for _ in self.OCTAVES]
        for i, h in enumerate(self.headings):
            self.headings[i] = h/np.linalg.norm(h)

        # voxel coordinates, built once
        axis = np.arange(10.0)
        self.grid = np.array(np.meshgrid(axis, axis, axis, indexing='ij'))

        # s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0

    def return_state(self):
        return [
            ['mode', 'mode', self.mode],
            ['speed', 'speed', round(self.speed,3)],
            ['scale', 'scale', round(self.scale,2)],
            ['channel', 'channel', self.channel],
        ]

    def __call__(self, args):
        # === PARAMETERS START ===
        self.mode = ['cloud', 'terrain'][int(args[0] > 0)]
        self.speed = args[1]*0.25+0.01
        self.scale = args[2]*7+2
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][int(args[3]*5)]
        # === PARAMETERS END ===

        speed = self.speed

        # check if S2L is activated
        if isinstance(self.channel, int):
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
            # the sound drives how fast the field moves, the knob is its ceiling.
            # clamped because past full volume the field jumps further than a
            # billow is wide each frame and the clouds break up into flicker
            speed = self.SPEED_MIN + min(current_volume, 1.0)*(self.speed - self.SPEED_MIN)

        #check for trigger
        elif self.channel == 'Trigger':
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            if current_volume > self.lastvalue:
                # send the field off in a new direction
                self.headings = [h/np.linalg.norm(h) for h in
                                 (np.random.uniform(-1, 1, 3) for _ in self.OCTAVES)]
            self.lastvalue = current_volume

        self.offset += speed

        field = np.zeros([10, 10, 10])
        total = 0.0

        for i, (size, weight) in enumerate(self.OCTAVES):
            # walk this octave through its own lattice, wrapping at the edges
            shift = self.headings[i] * self.offset[0]
            coords = self.grid/(self.scale*size) + shift.reshape(3, 1, 1, 1)

            field += weight * map_coordinates(self.lattices[i], coords,
                                              order=1, mode='grid-wrap')
            total += weight

        field /= max(total, 0.001)

        # stacked octaves of value noise pile up around the middle and barely
        # reach either end, so stretch whatever range it really used back out.
        # without this the cube is an even grey fog at about 85% lit.
        low, high = field.min(), field.max()
        field = (field - low)/max(high - low, 0.001)

        if self.mode == 'terrain':
            # read the field as a height map and light the surface it describes
            height = field[:, :, 0] * 9
            field = np.clip(1.4 - np.abs(self.grid[2] - height[:, :, None]), 0, 1)
        else:
            # keep the billows and drop the haze between them
            field = np.clip((field - 0.45)*2.6, 0, 1)

        # transfer to real world
        world = np.zeros([3, 10, 10, 10])
        for i in range(3):
            world[i, :, :, :] = field

        return np.clip(world, 0, 1)
