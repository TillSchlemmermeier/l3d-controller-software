# modules
import numpy as np
from scipy.ndimage.interpolation import rotate

class g_silpion():
    '''
    '''

    def __init__(self):
        self.original = np.zeros([10,10,10])
        for i in range(8):
            self.original[i+1, 4, 1:9-i] = 1

        self.xspeed = 0.1
        self.wobble_frames = 1000

        self.wobble = 100 # how long it wobbles
        self.wobble_count = 0

        self.wobble_amount = 20

    def control(self, xspeed, wobble, blub2):
        self.xspeed = 5*xspeed+0.01
        self.wobble_frames = int((wobble+0.1)*2000)
        self.wobble_amount = int((blub2+0.1)*90)

    def label(self):
        return ['speed', round(self.xspeed, 2),
                'wobble frames', self.wobble_frames,
                'wobble amount', self.wobble_amount]

    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

        # rotate
        newworld = rotate(self.original, step*self.xspeed,
                          axes = (1,2), order = 1,
	                      mode = 'nearest', reshape = False)

        # every self.wobble_frames do some wobble
        if step%self.wobble_frames == 0:
            self.wobble_count = 100

        # do wobble until counter is used upp
        if self.wobble_count > 0:
            newworld = rotate(newworld, self.wobble_amount*np.sin(self.wobble_count*np.pi*2*self.wobble),
                              axes = (1,2), order = 1,
    	                      mode = 'nearest', reshape = False)
            self.wobble_count -= 1

        # insert array
        world[0, :, :, :] = newworld
        world[1, :, :, :] = newworld
        world[2, :, :, :] = newworld

        return np.clip(world, 0, 1)
