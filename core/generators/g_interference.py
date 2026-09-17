# modules
import struct
import numpy as np
from multiprocessing import shared_memory


class g_interference():
    '''
    Generator: interference

    Three point sources orbiting inside the cube, each of them emitting a
    spherical wave. What you see is the sum of the three waves, a breathing
    standing wave lattice whose dark nodal shells slide through each other.

    Parameters:
    - wave   : wavelength, from fine grain to one big pulse
    - spread : how far the sources sit apart. below about 1.2 they overlap
               into one washed out glow, so that is where the knob starts
    - speed  : orbit and phase speed
    - s2l channel
    '''

    SOURCES = 3

    def __init__(self):
        self.wavelength = 4
        self.spread = 3
        self.speed = 0.15
        self.phase = 0
        # voxel coordinates, built once
        axis = np.arange(10)
        self.gx, self.gy, self.gz = np.meshgrid(axis, axis, axis, indexing='ij')
        # s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0

    def return_state(self):
        return [
            ['wavelength', 'wavelength', round(self.wavelength,2)],
            ['speed', 'speed', round(self.speed,2)],
            ['spread', 'spread', round(self.spread,2)],
            ['channel', 'channel', self.channel],
        ]

    def __call__(self, args):
        # === PARAMETERS START ===
        self.wavelength = args[0]*6+1.5
        self.speed = args[1]*0.25+0.02
        self.spread = args[2]*2.8+1.2
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][int(args[3]*5)]
        # === PARAMETERS END ===

        spread = self.spread

        # check if S2L is activated
        if isinstance(self.channel, int):
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
            # the sources fly apart with the volume
            spread = 1.2 + min(current_volume, 1.0)*2.8    # sources stay within the useful range

        #check for trigger
        elif self.channel == 'Trigger':
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            if current_volume > self.lastvalue:
                # flip the whole field over
                self.phase += np.pi
            self.lastvalue = current_volume

        self.phase += self.speed

        k = 2*np.pi / self.wavelength
        field = np.zeros([10, 10, 10])

        # sum up the spherical wave of every source
        for i in range(self.SOURCES):
            angle = self.phase*0.3 + i*2*np.pi/self.SOURCES
            sx = 4.5 + spread*np.cos(angle)
            sy = 4.5 + spread*np.sin(angle)
            sz = 4.5 + spread*np.sin(angle*0.7)

            dist = np.sqrt((self.gx-sx)**2 + (self.gy-sy)**2 + (self.gz-sz)**2)
            field += np.cos(k*dist - self.phase)

        # squaring turns the nodes into dark shells and the antinodes into light
        field /= self.SOURCES

        # transfer to real world
        world = np.zeros([3, 10, 10, 10])
        for i in range(3):
            world[i, :, :, :] = field * field

        return np.clip(world, 0, 1)
