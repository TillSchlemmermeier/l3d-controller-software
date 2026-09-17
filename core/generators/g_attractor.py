# modules
import struct
import numpy as np
from multiprocessing import shared_memory


class g_attractor():
    '''
    Generator: attractor

    A swarm of particles running along the Thomas strange attractor, drawn as
    fading trails. It is chaotic, so the path never repeats, but the swarm
    always keeps its own recognisable shape.

    Parameters:
    - number   : particles in the swarm
    - size     : 0 winds the swarm into a small tight knot, 1 lets it sprawl
    - fade     : how long the trails stay behind
    - s2l channel
    - s2l mode : whether the sound drives the speed or the size
    '''

    # damping constant of the Thomas system, parked in the middle of the band
    # where it stays chaotic. below about 0.105 the swarm sprawls, above 0.208
    # every particle runs into a fixed point and it freezes.
    DAMPING = 0.16
    # size is a straight scale on the positions instead of a change of damping.
    # damping only alters the forces, so the swarm needs a second or two to
    # actually spread out or draw in, which is far too slow to ride a beat.
    # scaling the positions lands on the very next frame.
    SCALE_SMALLEST = 0.40
    SCALE_BIGGEST = 1.12
    # euler step. the swarm crawls at DT_MIN and races at DT_MAX, which is the
    # largest step that still keeps it inside the +-5 box below
    DT_MIN = 0.06
    DT_MAX = 0.22
    # a beat sets the kick and it falls away, which gives the trigger the same
    # shape a band already has. it is set above 1 so a beat punches past what
    # the knobs alone can reach, the way a loud band does
    KICK_STRENGTH = 1.5
    KICK_DECAY = 0.85

    def __init__(self):
        self.number = 40
        self.size = 0.5
        self.s2l_mode = 'speed'
        self.kick = 0.0
        self.fade = 0.9
        self.points = np.random.uniform(-3, 3, [self.number, 3])
        self.trail = np.zeros([10, 10, 10])
        # s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0

    def return_state(self):
        return [
            ['number', 'number', self.number],
            ['size', 'size', round(self.size,2)],
            ['fade', 'fade', round(self.fade,2)],
            ['s2l mode', 's2l_mode', self.s2l_mode],
            ['channel', 'channel', self.channel],
        ]

    def scatter(self):
        '''throw the whole swarm back into the middle of the cube'''
        self.points = np.random.uniform(-3, 3, [self.number, 3])

    def __call__(self, args):
        # === PARAMETERS START ===
        self.number = int(args[0]*80)+10
        self.size = args[1]
        self.fade = args[2]*0.95
        self.s2l_mode = ['speed', 'size'][int(args[3] > 0)]
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][int(args[4]*5)]
        # === PARAMETERS END ===

        # how hard the sound is pushing right now. a band gives it straight,
        # the trigger turns each beat into a kick that falls away. None means
        # no sound is driving anything and the knobs are on their own.
        amount = None

        # check if S2L is activated
        if isinstance(self.channel, int):
            amount = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]

        #check for trigger
        elif self.channel == 'Trigger':
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            # decay first, so a beat lands on its full strength this frame
            self.kick *= self.KICK_DECAY
            if current_volume > self.lastvalue:
                self.kick = self.KICK_STRENGTH
            self.lastvalue = current_volume
            amount = self.kick

        size = self.size
        # without sound the swarm just runs at its top speed
        dt = self.DT_MAX

        # drive whichever one the s2l mode picked. nothing is capped at 1 here:
        # a loud enough band throws the swarm clean out of the cube, which is
        # allowed and looks better than pinning it to the walls
        if amount is None:
            pass
        elif self.s2l_mode == 'speed':
            dt = self.DT_MIN + amount*(self.DT_MAX-self.DT_MIN)
        else:
            # the knob sets where the swarm rests, the sound opens it up
            size = self.size + amount*(1 - self.size)

        scale = self.SCALE_SMALLEST + size*(self.SCALE_BIGGEST - self.SCALE_SMALLEST)

        # the knob was turned, rebuild the swarm
        if len(self.points) != self.number:
            self.scatter()

        # Thomas attractor, one euler step.
        # rolling the axis gives [sin(y), sin(z), sin(x)] for the three points
        self.points += dt * (np.sin(np.roll(self.points, -1, 1)) - self.DAMPING*self.points)
        # safety net only, inside the chaotic band the swarm never reaches this
        np.clip(self.points, -9, 9, out=self.points)

        # voxelise the swarm on top of the fading trails. the fade follows the
        # step size, otherwise a fast swarm sweeps more of the attractor between
        # fades and fills in denser, which reads as the thing having grown
        self.trail *= self.fade ** (dt/self.DT_MAX)
        voxel = ((self.points*scale + 5) * 0.9).astype(int)
        inside = np.all((voxel >= 0) & (voxel <= 9), axis=1)
        voxel = voxel[inside]
        self.trail[voxel[:,0], voxel[:,1], voxel[:,2]] = 1.0

        # transfer to real world
        world = np.zeros([3, 10, 10, 10])
        for i in range(3):
            world[i, :, :, :] = self.trail

        return np.clip(world, 0, 1)
