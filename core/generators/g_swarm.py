# modules
import struct
import numpy as np
from multiprocessing import shared_memory


class g_swarm():
    '''
    Generator: swarm

    A murmuration. Every bird steers by three urges at once: keep off its
    neighbours, fly the way they fly, and stay with the group. Every other
    particle generator here moves its particles independently, so this is the
    only one where the shape of the flock is nobody's decision. It never
    repeats and it never settles.

    Parameters:
    - number    : size of the flock
    - cohesion  : loose scattered swarm through to one tight ball
    - fade      : how long the birds smear behind them
    - s2l channel : the sound opens the flock out and lets it close again
    '''

    MAX_BIRDS = 60
    # birds fly at a steady pace, only their heading changes
    SPEED = 0.42
    # the sound scales the drawn positions about the middle of the flock rather
    # than changing the flocking forces. a force needs a second or two before
    # the flock has actually moved, which is far too slow to ride a beat
    SCALE_SMALLEST = 0.35
    SCALE_BIGGEST = 1.35
    # a beat sets the kick and it falls away. above 1 so a beat punches past
    # what the sound alone reaches, the way a loud band does
    KICK_STRENGTH = 1.5
    KICK_DECAY = 0.85
    # a bird only reacts to what is inside this range
    VIEW = 3.0

    def __init__(self):
        self.number = 30
        self.cohesion = 0.5
        self.fade = 0.8
        self.kick = 0.0

        self.points = np.random.uniform(1, 8, [self.MAX_BIRDS, 3])
        self.velocity = np.random.uniform(-1, 1, [self.MAX_BIRDS, 3])
        self.trailworld = np.zeros([10, 10, 10])

        # s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0

    def return_state(self):
        return [
            ['number', 'number', self.number],
            ['cohesion', 'cohesion', round(self.cohesion,2)],
            ['fade', 'fade', round(self.fade,2)],
            ['channel', 'channel', self.channel],
        ]

    def __call__(self, args):
        # === PARAMETERS START ===
        self.number = int(args[0]*(self.MAX_BIRDS-8))+8
        self.cohesion = args[1]
        self.fade = args[2]
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][int(args[3]*5)]
        # === PARAMETERS END ===

        cohesion = self.cohesion

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

        # without sound the flock is drawn as it is. nothing is capped at 1
        # here: a loud enough band throws it clean out of the cube
        scale = 1.0
        if amount is not None:
            scale = self.SCALE_SMALLEST + amount*(self.SCALE_BIGGEST - self.SCALE_SMALLEST)

        p = self.points[:self.number]
        v = self.velocity[:self.number]

        # every bird against every other one. the flock is small enough that
        # the full table is cheaper than any clever way of avoiding it
        offset = p[None, :, :] - p[:, None, :]
        distance = np.linalg.norm(offset, axis=2)
        neighbour = (distance < self.VIEW) & (distance > 0)
        count = neighbour.sum(axis=1, keepdims=True)
        has_company = count[:, 0] > 0

        weights = neighbour[:, :, None]
        safe_count = np.maximum(count, 1)

        # stay with the group, and fly the way it flies
        centre = (offset*weights).sum(axis=1) / safe_count
        matched = ((v[None, :, :]*weights).sum(axis=1) / safe_count) - v

        # keep out of each other's way, hardest when closest
        crowding = neighbour & (distance < self.VIEW*0.5)
        push = -(offset*crowding[:, :, None]).sum(axis=1)

        steer = 0.08*cohesion*centre + 0.05*matched + 0.06*push
        steer[~has_company] = 0

        # turn back before hitting a wall rather than bouncing off it
        # gentle, so it nudges them round rather than pinning them to the middle
        steer += 0.04*np.clip(1.5 - p, 0, None) - 0.04*np.clip(p - 7.5, 0, None)

        v += steer

        # birds fly at a steady speed, only their heading changes
        pace = np.linalg.norm(v, axis=1, keepdims=True)
        v *= self.SPEED / np.maximum(pace, 0.001)

        p += v
        np.clip(p, 0, 9, out=p)

        self.points[:self.number] = p
        self.velocity[:self.number] = v

        # draw the flock over its own fading trails
        self.trailworld *= self.fade

        # scale about the middle of the flock, so size opens it out in place
        middle = p.mean(axis=0)
        drawn = middle + (p - middle)*scale

        voxel = drawn.astype(int)
        inside = np.all((voxel >= 0) & (voxel <= 9), axis=1)
        voxel = voxel[inside]
        self.trailworld[voxel[:, 0], voxel[:, 1], voxel[:, 2]] = 1.0

        # transfer to real world
        world = np.zeros([3, 10, 10, 10])
        for i in range(3):
            world[i, :, :, :] = self.trailworld

        return np.clip(world, 0, 1)
