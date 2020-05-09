# modules
import numpy as np

class e_bright_osci():
    '''
    Effect: tremolo
    '''

    def __init__(self):
        self.speed = 1.0
        self.shape = 1.0
        self.step = 0

    #strings for GUI
    def return_values(self):
        return [b'bright_osci', b'speed', b'shape', b'', b'']


    def __call__(self, world, args):
        # parsing input
        self.speed = args[0]*2-1
        self.shape = args[1]*3+0.001

        # modulate brightness
        for x in range(10):
            world[:,x,:,:] *= np.sin(self.speed*self.step+x)

        # compressor for SHAPE
        world[:,:,:,:] = np.clip(world[:,:,:,:],0,1)**self.shape

        self.step += 1

        return world
