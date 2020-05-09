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

    def control(self, speed, shape, amplitude):
        self.speed = speed*2-1
        self.shape = shape*3+0.001

    def generate(self, step, world):

        # modulate brightness
        for x in range(10):
            world[:,x,:,:] *= np.sin(self.speed*self.step+x)

        # compressor for SHAPE
        world[:,:,:,:] = np.clip(world[:,:,:,:],0,1)**self.shape

        self.step += 1

        return np.clip(world, 0, 1)
