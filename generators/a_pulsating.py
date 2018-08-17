# modules
import numpy as np
from random import choice, uniform
from generators.g_genhsphere import gen_hsphere
from colorsys import rgb_to_hsv, hsv_to_rgb


class a_pulsating():
    '''
    Automat: pulsating
    '''

    def __init__(self):
        self.counter = 0
        self.period = 200
	self.start_strobo = 10
	self.strobo_counter = 20
	
        # initialize generator
        self.generator = g_cube()
        self.generator.control(1,0.11,1)
        
        self.color =  hsv_to_rgb(uniform(-0.5,0.5), 1.0, 1.0)
                
    def control(self, count_fade, fade, blub1):
        #self.count_fade = int(count_fade * 200)+50)
	pass
	
    def label(self):
        return ['empty', 'empty',
                'empty', 'empty',
                'empty', 'empty']

    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])
        
        size = np.sin(self.counter / self.period * np.pi)*6
        brightness  = np.sin(self.counter / self.period * np.pi)**6
        
        world[0, :, :, :] = gen_hsphere(size, 5.5, 5.5, 5.5) * brightness
        world[1:, :, :, :] = world[0, :, :, :]
        world[2:, :, :, :] = world[0, :, :, :]

	# color
	if self.counter % self.period == 0:
	    self.color =  hsv_to_rgb(uniform(-0.5,0.5), 1.0, 1.0)

        world[0,:,:,:] *= color[0]
        world[1,:,:,:] *= color[1]
        world[2,:,:,:] *= color[2]
        
        if self.counter > self.start_strobo*self.peroid and self.counter < self.start_strobo*self.peroid+self.strobo_counter:
            size = 0.0
            if self.counter % 2 == 1:
                world[0, :, : ,:] = gen_hsphere(size*8, 5.5, 5.5, 5.5)
            
            size += 1/self.strobo_counter
            
        self.counter += 1
        
        return np.clip(world, 0, 1)

