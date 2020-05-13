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
        self.amplitude = 1.0
        self.step = 0

    #strings for GUI
    def return_values(self):
        return [b'tremolo', b'speed', b'shape (sin/square/up/down)', b'amplitude', b'']

    def __call__(self, world, args):
		# parse input
        self.speed = args[0]*3
        if args[1] < 0.25:
            self.shape = 'sin'
        elif args[1] >= 0.25 and args[1] < 0.5:
            self.shape = 'square'
        elif args[1] >= 0.5 and args[1] < 0.75:
            self.shape = 'up'
        else:
            self.shape = 'down'

        self.amplitude = args[2]

        # modulate brightness
        if self.shape == 'sin':
            world[:,:,:,:] *= (1-self.amplitude) + self.amplitude * np.sin(self.step*np.pi*self.speed*0.1)
        elif self.shape == 'square':
            world[:,:,:,:] *= (1-self.amplitude) + self.amplitude * square(self.step*np.pi*self.speed*0.1)
        elif self.shape == 'up':
            world[:,:,:,:] *= (1-self.amplitude) + self.amplitude * sawtooth(self.step*np.pi*self.speed*0.1, width = 1)
        else:
            world[:,:,:,:] *= (1-self.amplitude) + self.amplitude * sawtooth(self.step*np.pi*self.speed*0.1, width = 0)

        self.step += 1
        return np.clip(world, 0, 1)
