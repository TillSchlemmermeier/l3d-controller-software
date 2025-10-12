import numpy as np

class e_invert():
    '''Effect: inverts everything'''

    def __init__(self):
        self.on = True
        self.oldworld = np.zeros([3, 10, 10, 10])

    def return_state(self):
        # return [Display Name, Viariable Name, Display Value] for each parameter
        return [
            ['ON', 'on', round(self.on,1)],
        ]

    def __call__(self, world, args):
		# parse input
        if args[0] > 0.5:
            self.on = True
        else:
            self.on = False

        if self.on:
            world *= -1
        
        return np.clip(world, -1, 1)
