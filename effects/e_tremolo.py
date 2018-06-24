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
        self.speed = speed*2
        self.shape = shape*3+0.001
        self.amplitude = amplitude

    def label(self):
        return ['Speed', round(self.speed,2),
                'Shape', round(self.shape,2),
                'Amplitude',round(self.amplitude,2)]

    def generate(self, step, world):

        # modulate brightness
        world[:,:,:,:] *= self.amplitude * np.sin(step*np.pi*self.speed*0.1)

        # compressor for SHAPE
        # world[:,:,:,:] = world[:,:,:,:]**self.shape

        return np.clip(world, 0, 1)
