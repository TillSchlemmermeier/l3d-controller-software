# modules
import numpy as np
from scipy.signal import square, sawtooth

class e_tremolo():
    '''
    Effect: tremolo
    '''

    def __init__(self):
        self.speed = 1.0
        self.shape = 1.0
        self.amplitude = 0.5

    def control(self, speed, shape, amplitude):
        self.speed = speed*3
        # self.shape = shape*3+0.001
        if shape < 0.25:
            self.shape = 'sin'
        elif shape >= 0.25 and shape < 0.5:
            self.shape = 'square'
        elif shape >= 0.5 and shape < 0.75:
            self.shape = 'up'
        else:
            self.shape = 'down'

        self.amplitude = amplitude

    def label(self):
        return ['Speed', round(self.speed,2),
                'Shape', self.shape,
                'Amplitude',round(self.amplitude,2)]

    def generate(self, step, world):

        # modulate brightness
        if self.shape == 'sin':
            world[:,:,:,:] *= self.amplitude * np.sin(step*np.pi*self.speed*0.1)
        elif self.shape == 'square':
            world[:,:,:,:] *= self.amplitude * square(step*np.pi*self.speed*0.1)
        elif self.shape == 'up':
            world[:,:,:,:] *= self.amplitude * sawtooth(step*np.pi*self.speed*0.1, width = 1)
        else:
            world[:,:,:,:] *= self.amplitude * sawtooth(step*np.pi*self.speed*0.1, width = 0)

        return np.clip(world, 0, 1)
