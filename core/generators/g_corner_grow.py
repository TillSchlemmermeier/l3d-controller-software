import numpy as np
from multiprocessing import shared_memory

class g_corner_grow():
    '''
    Generator: corner_grow

    '''

    def __init__(self):
        self.mode = 'sync'
        self.waiting = 10
        self.trigger = False
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.lastvalue = 0

        self.corners = [
            {'pos': (4, 4, 4), 'size': None},
            {'pos': (4, 4, 5), 'size': None},
            {'pos': (4, 5, 4), 'size': None},
            {'pos': (4, 5, 5), 'size': None},
            {'pos': (5, 4, 4), 'size': None},
            {'pos': (5, 4, 5), 'size': None},
            {'pos': (5, 5, 4), 'size': None},
            {'pos': (5, 5, 5), 'size': None},
        ]
        self.current_corner = 0
        self.step = 0

    def return_state(self):
        return [
            ['mode', 'mode', self.mode],
            ['waiting', 'waiting', round(self.waiting,2)],
            ['trigger', 'trigger', self.trigger],
        ]

    def __call__(self, args):
        # === PARAMETERS START ===
        self.mode = ['sync', 'seq', 'random'][int(round(args[0]*2))]
        self.waiting = int(args[1]*50)+1
        self.trigger = args[2] >= 0.5
        # === PARAMETERS END ===

        # create world
        world = np.zeros([3, 10, 10, 10])

        if not self.trigger:
            if self.step == 0:
                if self.mode == 'seq':
                    self.current_corner = (self.current_corner + 1) % 8
                    self.corners[self.current_corner]['size'] = 0
                elif self.mode == 'random':
                    self.current_corner = np.random.randint(0, 8)
                    self.corners[self.current_corner]['size'] = 0
                else:
                    for corner in self.corners:
                        corner['size'] = 0

        else:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                
                for corner in self.corners:
                    corner['size'] = 0

        for corner in self.corners:
            size = corner['size']
            if type(size) == int:
                x, y, z = corner['pos']
                if x == 4:
                    x = 4 - size
                else:
                    x = 5 + size
                if y == 4:
                    y = 4 - size
                else:
                    y = 5 + size
                if z == 4:
                    z = 4 - size
                else:
                    z = 5 + size
                world[:, x, y, z] = 1.0

                if corner['size'] < 4:
                    corner['size'] += 1
                else:
                    corner['size'] = None
        
        self.step += 1
        if self.step >= self.waiting:
            self.step = 0

        return np.clip(world, 0, 1)
