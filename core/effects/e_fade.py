# modules
import numpy as np

class e_fade():
    '''Effect: zoom'''

    def __init__(self):
        self.amount = 0.5
        self.oldworld = np.zeros([3, 10, 10, 10])

    def return_state(self):
        # return [Display Name, Viariable Name, Display Value] for each parameter
        return [
            ['amount', 'amount', round(self.amount,1)],
        ]

    def __call__(self, world, args):
		# parse input
        self.amount = args[0]

        world += self.oldworld*self.amount
        self.oldworld[:, :, :, :] = world[:, :, :, :]

        return np.clip(world, 0, 1)
