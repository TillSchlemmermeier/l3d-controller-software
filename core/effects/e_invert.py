import numpy as np

class e_invert():
    '''Effect: inverts everything'''

    def __init__(self):
        self.on = True
        self.oldworld = np.zeros([3, 10, 10, 10])

    def return_state(self):
        return [
            ['ON', 'on', str(self.on)],
        ]

    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.on = args[0] > 0.5
        # === PARAMETERS END ===

        if self.on:
            world *= -1
        
        return np.clip(world, -1, 1)
