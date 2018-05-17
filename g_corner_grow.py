
import numpy as np


class g_corner_grow():
    '''
    Generator: corner_grow

    '''

    def __init__(self):
        self.waiting = 10
        self.size = 0
        self.speed = 0

        self.waitingcounter = 0

    def control(self, speed, waiting, dump):
        self.speed = speed
        self.waiting = int(waiting*50)

    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

        if self.size > 4.0
            # switch into waiting state
            self.waitingcounter = self.waiting
            self.size = 0

        elif self.waitingcounter == 0:
            if step%self.speed == 0:
                # switch on corners

		world[:,4-self.size,4-self.size,4-self.size] = 1.0
		world[:,4-self.size,4-self.size,5+self.size] = 1.0
		world[:,4-self.size,5+self.size,4-self.size] = 1.0
		world[:,5+self.size,4-self.size,4-self.size] = 1.0
		world[:,4-self.size,5+self.size,5+self.size] = 1.0
		world[:,5+self.size,4-self.size,5+self.size] = 1.0
		world[:,5+self.size,5+self.size,4-self.size] = 1.0
		world[:,5+self.size,5+self.size,5+self.size] = 1.0
	
        	self.size += 1

        else:
            # stay in waiting state
            self.waitingcounter -= 1:

        return np.clip(world, 0, 1)

