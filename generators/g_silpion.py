# modules
import numpy as np
from scipy.ndimage.interpolation import rotate

class g_silpion():
    '''
    '''

    def __init__(self):
        self.original = np.zeros([10,10,10])
        for i in range(9):
            self.original[4, i,1:i] = 1
            
        self.xspeed = 0.1
        self.wobble_frames = 1000
        
        self.wobble = 100 # how long it wobbles
        self.wobble_count = 0


    def control(self, xspeed, wobble, blub2):
        self.xspeed = xspeed+0.01
        self.wobble_frames = int(wobble*2000)


    def label(self):
        return ['size', round(self.xspeed, 2),
                'wobble frames', self.wobble_frames,
                'empty', 'empty']


    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

	# rotate
	newworld = rotate(self.orginal, step*self.xspeed,
	                  axes = (1,2), order = 1,
	                  mode = 'nearest', reshape = False
	                  
	# every self.wobble_frames do some wobble
	if step%self.wobble_frames == 0:
	    self.wobble_count = 100
	
	# do wobble until counter is used upp
	if self.wobble_count > 0:
	    newworld = rotate(newworld, np.sin(self.wobble_count*np.pi*2*self.wooble))
	    self.wobble_count -= 1
	
	# insert array
	world[0, :, :, :] = newworld
	world[1, :, :, :] = newworld	
	world[2, :, :, :] = newworld
		
        return np.clip(world, 0, 1)
