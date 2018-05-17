
import numpy as np


class g_corner():
    '''
    Generator: corner

    '''


    def __init__(self):
        self.blub = 0

    def control(self, blub0, blub1, blub2):
        self.blub = 0

    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

	# switch on corners
	world[:,0,0,0] = 1.0
	world[:,0,0,9] = 1.0
	world[:,0,9,0] = 1.0
	world[:,9,0,0] = 1.0
	world[:,0,9,9] = 1.0
	world[:,9,0,9] = 1.0
	world[:,9,9,0] = 1.0
	world[:,9,9,9] = 1.0

        return np.clip(world, 0, 1)

