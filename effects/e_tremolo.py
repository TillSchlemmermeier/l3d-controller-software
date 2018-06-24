# modules
import numpy as np

class e_tremolo():
    '''
    Effect: tremolo
    '''

    def __init__(self):
        self.speed = 1.0
        self.shape = 1.0
        self.amplitude = 0.5

    def control(self, speed, shape, amplitude):
        self.speed = speed
        self.shape = shape+2.0
        self.amplitude = amplitude

    def label(self):
        return ['SPEED', self.speed,
                'SHAPE', self.shape,
                'AMPLITUDE',self.amplitude]

    def generate(self, step, world):

        # modulate brightness
        world[:,:,:,:] *= self.amplitude * np.sin(step*np.pi*speed*0.1)

        # compressor for SHAPE
        world[:,:,:,:] = world[:,:,:,:]**self.shape

        return np.clip(world, 0, 1)
