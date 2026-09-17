# modules
import struct
import numpy as np
from multiprocessing import shared_memory


class g_shapes():
    '''
    Generator: shapes

    A platonic solid turning in the middle of the cube, drawn as glowing
    edges. g_cube_edges is the only other wireframe here and it only ever
    draws a cube. Thin bright lines read far better on ten voxels than a
    filled shape does, which just turns into a lump.

    Parameters:
    - solid     : tetrahedron, octahedron, cube or icosahedron
    - speed     : how fast it turns
    - thickness : how fat the edges are drawn
    - size      : how much of the cube it fills
    - s2l channel
    '''

    # the order the beat walks through the shapes
    SOLIDS = ['tetra', 'octa', 'cube', 'icosa']
    # what size 0 and size 1 mean once the shape is actually drawn. 4.7 puts the
    # vertices just past the walls, which fills the cube without losing them
    SIZE_SMALLEST = 1.5
    SIZE_BIGGEST = 4.7
    # a beat swells the solid by this much and spins it this many times faster,
    # both fading out again. the swell is allowed a little past the biggest the
    # knob reaches, otherwise a beat does nothing at all with size wound up full
    KICK_SWELL = 0.55
    KICK_SPIN = 4.0
    KICK_DECAY = 0.82
    SIZE_OVERSHOOT = 1.25
    # beats between shape changes. every beat is far too fast to make out which
    # solid is actually turning
    BEATS_PER_SOLID = 4

    def __init__(self):
        self.solid = 'tetra'
        self.speed = 0.03
        self.thickness = 0.9
        self.size = 0.7
        self.angle = 0.0

        self.shapes = {
            'tetra': self._tetra(),
            'octa': self._octa(),
            'cube': self._cube(),
            'icosa': self._icosa(),
        }

        # every voxel centre as a flat list, built once
        axis = np.arange(10.0)
        self.voxels = np.stack(np.meshgrid(axis, axis, axis, indexing='ij'),
                               axis=-1).reshape(-1, 3)

        # s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0
        self.kick = 0.0
        self.beats = 0
        self.turns = 0

    def return_state(self):
        return [
            ['solid', 'solid', self.solid],
            ['size', 'size', round(self.size,2)],
            ['speed', 'speed', round(self.speed,3)],
            ['thick', 'thickness', round(self.thickness,2)],
            ['channel', 'channel', self.channel],
        ]

    def _normalise(self, verts, edges):
        '''scale a solid so all its vertices sit on the unit sphere'''
        verts = np.array(verts, dtype=float)
        verts /= np.linalg.norm(verts, axis=1, keepdims=True).max()
        return verts, np.array(edges)

    def _tetra(self):
        v = [[1,1,1], [1,-1,-1], [-1,1,-1], [-1,-1,1]]
        e = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]
        return self._normalise(v, e)

    def _octa(self):
        v = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]]
        e = [[0,2],[0,3],[0,4],[0,5],[1,2],[1,3],[1,4],[1,5],
             [2,4],[2,5],[3,4],[3,5]]
        return self._normalise(v, e)

    def _cube(self):
        v = [[x,y,z] for x in (-1,1) for y in (-1,1) for z in (-1,1)]
        e = [[i,j] for i in range(8) for j in range(i+1, 8)
             if np.abs(np.array(v[i])-np.array(v[j])).sum() == 2]
        return self._normalise(v, e)

    def _icosa(self):
        g = (1 + 5**0.5)/2
        v = []
        for s1 in (-1, 1):
            for s2 in (-1, 1):
                v += [[0, s1, s2*g], [s1, s2*g, 0], [s2*g, 0, s1]]
        v = np.array(v, dtype=float)
        # an icosahedron's edges are exactly the closest vertex pairs
        shortest = min(np.linalg.norm(v[i]-v[j])
                       for i in range(len(v)) for j in range(i+1, len(v)))
        e = [[i,j] for i in range(len(v)) for j in range(i+1, len(v))
             if np.linalg.norm(v[i]-v[j]) < shortest*1.1]
        return self._normalise(v, e)

    def __call__(self, args):
        # === PARAMETERS START ===
        self.solid = self.SOLIDS[min(int(args[0]*4), 3)]
        self.size = args[1]
        self.speed = args[2]*0.09+0.005
        self.thickness = args[3]*1.3+0.5
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][int(args[4]*5)]
        # === PARAMETERS END ===

        size = self.size
        speed = self.speed

        # check if S2L is activated
        if isinstance(self.channel, int):
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
            # the knob is the smallest the solid is ever drawn and the sound
            # grows it from there, uncapped. a loud enough hit pushes the
            # vertices out through the walls, which is the point
            size = self.size + current_volume

        #check for trigger
        elif self.channel == 'Trigger':
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            self.kick *= self.KICK_DECAY      # decay first, so a beat lands at full strength
            if current_volume > self.lastvalue:
                self.kick = 1.0
                self.beats += 1
                if self.beats % self.BEATS_PER_SOLID == 0:
                    self.turns += 1
            self.lastvalue = current_volume

            # the solid jumps out and lurches round on the hit, then settles back
            size = min(self.size + self.kick*self.KICK_SWELL, self.SIZE_OVERSHOOT)
            speed = self.speed * (1 + self.kick*self.KICK_SPIN)

        # the beat walks the shape on from whichever one the knob picked. the
        # parameter block above rewrites self.solid every frame, so the walk has
        # to be kept as a count of turns rather than as the shape itself
        self.solid = self.SOLIDS[(self.SOLIDS.index(self.solid) + self.turns) % 4]

        self.angle += speed
        verts, edges = self.shapes[self.solid]

        # turn about two axes at once so it never presents a flat face for long
        ca, sa = np.cos(self.angle), np.sin(self.angle)
        cb, sb = np.cos(self.angle*0.61), np.sin(self.angle*0.61)
        spin_z = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]])
        spin_x = np.array([[1, 0, 0], [0, cb, -sb], [0, sb, cb]])

        scale = self.SIZE_SMALLEST + size*(self.SIZE_BIGGEST - self.SIZE_SMALLEST)
        turned = verts @ spin_z.T @ spin_x.T * scale + 4.5

        # how far every voxel sits from the nearest edge. splatting samples
        # along the edges instead only ever lights the one voxel the line runs
        # through, and the knob then reads as brightness rather than as width
        starts = turned[edges[:, 0]]
        along = turned[edges[:, 1]] - starts

        # project each voxel onto each edge, held inside the segment's own ends
        offset = self.voxels[None, :, :] - starts[:, None, :]
        travel = np.clip(np.einsum('evi,ei->ev', offset, along)
                         / np.maximum(np.einsum('ei,ei->e', along, along), 1e-6)[:, None], 0, 1)
        gap = offset - travel[:, :, None]*along[:, None, :]
        distance = np.sqrt(np.einsum('evi,evi->ev', gap, gap)).min(axis=0)

        # full brightness on the line itself, fading out over the thickness
        field = np.clip(1 - distance.reshape(10, 10, 10)/self.thickness, 0, 1)

        # transfer to real world
        world = np.zeros([3, 10, 10, 10])
        for i in range(3):
            world[i, :, :, :] = field

        return np.clip(world, 0, 1)
