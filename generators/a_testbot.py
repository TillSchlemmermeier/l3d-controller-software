# modules
import numpy as np
from g_cube import g_cube

class a_testbot():
    '''
    Generator: Testbot
    '''

    def __init__(self):
        self.counter = 1

    def control(self, numbers, fade, blub1):
	pass
	
    def label(self):
        return ['empty', 'empty',
                'empty', 'empty',
                'empty', 'empty']
                
    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])
        
        generator = g_cube()

        if counter <= 1000:
            generator.control(4,1,0)
            self.counter += 1
        elif counter > 1000 and counter <= 2000:
            generator.control(3,1,0)
            self.counter += 1
        if counter > 2000:
            self.counter = 0

	world[0,:,:,:] = generator.generate(self.counter, 0)

        return np.clip(world, 0, 1)
