# modules
import numpy as np
from scipy.signal import square, sawtooth

class e_tremolo():
    '''
    Effect: tremolo
    '''

    def __init__(self):
        self.speed = 1.0
        self.shape = 'down'
        self.amplitude = 1.0
        self.step = 0

    def return_state(self):
        return [
            ['speed', 'speed', round(self.speed,1)],
            ['shape', 'shape', self.shape],
            ['ampli', 'amplitude', round(self.amplitude,1)],
        ]

    def __call__(self, world, args):
		# === PARAMETERS START ===
        self.speed = args[0]*3
        self.shape = ['sin', 'square', 'up', 'down'][round(args[1]*3)]
        self.amplitude = args[2]
        # === PARAMETERS END ===

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
