# modules
import numpy as np
from random import randint

class g_drop():

    class drop():
        
        def __init__(self):
            self.x = 0
            self.y = randint(0,9)
            self.z = randint(0,9)
            
            self.brightness = 0.0
            
            self.state = 0
            self.counter = 0
        
    	def do_step(self):
    	
    	    temp = [self.x, self.y, self.z, self.brightness, self.state]
    	    
    	    # do stuff
    	    if self.state == 0:
    	        self.brightness += 0.1
    	        
    	    elif self.state == 1:
    	        self.x += 1
    	        
    	    elif self.state == 2:
    	        self.brightness -= 0.1
    	        
    	    # update state
    	    if self.brightness => 1.0 and self.state == 0:
    	        self.state = 1
    	        
    	    elif self.x <= 9:
    	        self.state = 2
    	        
    	    elif self.brightness <= 0.0 and self.state == 2:
    	        self.state = 3
    	    
    	    return temp

    '''
    Generator: drop
    '''

    def __init__(self):
        self.numbers = 1
        self.drops = []
        self.drops.append(drop())
        
    def control(self, numbers, blub0, blub1):
        self.numbers = int(numbers*10 + 1)
        self.numbers = 1

    def label(self):
        return ['Numbers', self.numbers,
                'empty', 'empty',
                'empty', 'empty']

    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])
	
	# do step
	for i in range(self.numbers):
	    [x, y, z, b, s] = self.drops[i].do_step()
	    world[:,x,y,z] = b
	    if s == 4:
	        del(self.drops())
	        self.drops.append(drop)
	    

        return np.clip(world, 0, 1)
