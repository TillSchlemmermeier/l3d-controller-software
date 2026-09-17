# modules
import struct
import numpy as np
from random import randint
from multiprocessing import shared_memory


class g_ripple():
    '''
    Generator: ripple

    A real wave equation solved inside the cube. An impulse is dropped in, the
    ripple travels outwards and reflects off all six walls. The next drop only
    falls once that one has faded away, so what you see interferes with its own
    reflections and not with a crowd of older drops.

    Parameters:
    - speed   : how fast the wave travels
    - damping : how quickly the cube goes quiet again
    - impulse : strength of a single drop
    - s2l channel
    '''

    # runaway guard only, well clear of the loudest drop the knobs allow
    CEILING = 30.0
    # a new ripple waits for the field to fall below this. waiting for it to
    # vanish outright leaves the cube dark about half the time, faint is the
    # line that keeps it busy without letting drops pile up on each other
    QUIET = 0.15
    # how much of the field the water level is allowed to hide. at silence only
    # the tallest crests clear it and the cube shows bare wave fronts, at full
    # volume the level drops to zero and the whole ripple floods into view
    LEVEL_SPAN = 0.6

    def __init__(self):
        self.speed = 0.08
        self.damping = 0.99
        self.impulse = 4
        # wave field and its velocity
        self.p = np.zeros([10, 10, 10])
        self.vel = np.zeros([10, 10, 10])
        # padded buffer for the reflecting walls, allocated once
        self.pad = np.zeros([12, 12, 12])
        # voxel coordinates, used to shape a drop
        axis = np.arange(10)
        self.gx, self.gy, self.gz = np.meshgrid(axis, axis, axis, indexing='ij')
        # s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0

    def return_state(self):
        return [
            ['impulse', 'impulse', round(self.impulse,2)],
            ['speed', 'speed', round(self.speed,3)],
            ['damping', 'damping', round(self.damping,3)],
            ['channel', 'channel', self.channel],
        ]

    # width of a drop. a single voxel is a sharp spike that holds every spatial
    # frequency at once and scatters into noise within a few frames, a soft blob
    # keeps the wave front together long enough to watch it hit a wall
    SIGMA = 1.5

    def drop(self, amount):
        '''push the field up in a soft blob around a random spot'''
        x, y, z = randint(2,7), randint(2,7), randint(2,7)
        dist2 = (self.gx-x)**2 + (self.gy-y)**2 + (self.gz-z)**2
        self.p += amount * np.exp(-dist2/(2*self.SIGMA**2))

    def laplacian(self):
        '''6 neighbour laplacian with edge clamped walls, so the waves reflect'''
        pad = self.pad
        pad[1:-1, 1:-1, 1:-1] = self.p
        pad[0] = pad[1]
        pad[-1] = pad[-2]
        pad[:, 0] = pad[:, 1]
        pad[:, -1] = pad[:, -2]
        pad[:, :, 0] = pad[:, :, 1]
        pad[:, :, -1] = pad[:, :, -2]

        return (pad[2:, 1:-1, 1:-1] + pad[:-2, 1:-1, 1:-1]
              + pad[1:-1, 2:, 1:-1] + pad[1:-1, :-2, 1:-1]
              + pad[1:-1, 1:-1, 2:] + pad[1:-1, 1:-1, :-2]
              - 6 * self.p)

    def __call__(self, args):
        # === PARAMETERS START ===
        self.impulse = args[0]*6+1
        self.speed = args[1]*0.09+0.04
        self.damping = 1 - (args[2]*0.022+0.003)
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][int(args[3]*5)]
        # === PARAMETERS END ===

        # the last ripple has faded, so the cube is free to take a new one
        settled = np.abs(self.p).max() < self.QUIET
        volume = None

        # check if S2L is activated
        if isinstance(self.channel, int):
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
            # the band decides how much of the wave is shown, not how it moves.
            # anything routed through the physics trails the music by a dozen
            # frames, a threshold on the way out lands on the beat. applied
            # below, once this frame's field exists
            volume = min(current_volume, 1.0)
            if settled:
                self.drop(self.impulse)

        #check for trigger
        elif self.channel == 'Trigger':
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            if current_volume > self.lastvalue:
                # a beat lands when it lands, it does not queue behind the gate.
                # wipe whatever is still ringing so the new ripple starts clean
                self.p[:] = 0
                self.vel[:] = 0
                self.drop(self.impulse)
            self.lastvalue = current_volume

        # free running, one ripple at a time
        elif settled:
            self.drop(self.impulse)

        # integrate the wave equation
        self.vel += self.speed * self.laplacian()
        self.vel *= self.damping
        self.p += self.vel

        # fade the field itself, not only its velocity. an older ripple has to
        # clear out of the way or the newer ones cannot be made out at all
        self.p *= self.damping

        # the walls reflect, so the laplacian sums to zero and the average level
        # of the field is conserved. damping only takes energy out of the
        # velocity, which leaves every drop raising that average a little more
        # until the whole cube sits at one flat bright level. take it back out.
        self.p -= self.p.mean()

        # a live show runs for hours, never let the field run away. this sits
        # far above anything the impulse knob reaches on purpose: everything
        # else here is linear, so as long as nothing clips, how fast a ripple
        # dies is the damping knob's business alone. clamping inside the
        # working range made a loud drop look heavily damped.
        np.clip(self.p, -self.CEILING, self.CEILING, out=self.p)

        # a water level the sound raises and lowers. measured against this
        # frame's own peak, so it keeps revealing the same share of the wave as
        # the ripple decays instead of swallowing it whole halfway through
        level = 0.0
        if volume is not None:
            level = np.abs(self.p).max() * self.LEVEL_SPAN * (1 - volume)

        # only the crests, not the troughs. taking the absolute value draws
        # every wave twice over and the fronts disappear in the clutter
        crest = np.clip(self.p - level, 0, None)

        # transfer to real world
        world = np.zeros([3, 10, 10, 10])
        for i in range(3):
            world[i, :, :, :] = crest

        return np.clip(world, 0, 1)
