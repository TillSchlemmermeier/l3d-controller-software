# modules
import numpy as np

class e_fade2blue():
    '''
    Effect: fade2blue

    fades the cube to blue by moving some of the green and red
    to the blue

    Parameters:
    - amount: how much is moved from the r/g channel to the b channel
    '''

    def __init__(self):
        self.amount = 0.5


    def control(self, amount, blub0, blub1):
        self.amount = amount


    def generate(self, world):
        world[2, :, :, :] += self.amount*world[:2, :, :, :]
        world[:2, :, :, :] -= world[:2, :, :, :]*self.amount

        return np.clip(world,0,1)
