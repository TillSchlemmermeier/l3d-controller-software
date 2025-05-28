# modules
import numpy as np
from multiprocessing import shared_memory

class e_bright_mod():
    '''
    Effect: modulation of brightness
    '''

    def __init__(self):
        self.speed = 1.0
        self.amount = 0.5
        self.step = 0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 4
        self.wavelength = 0.1
        self.spread = 0

    def return_state(self):
        if self.channel >= 0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return [
            ['speed', 'speed', round(self.speed,2)],
            ['amount', 'amount', round(self.amount,2)],
            ['spread', 'spread', round(self.spread,2)],
            ['channel', 'channel', channel],
        ]
    
    def __call__(self, world, args):
        # parsing input
        self.speed   = args[0]*0.1 + 0.001
        self.amount  = args[1]
        self.spread  = args[2]*0.01
        self.channel = int(args[3]*4)-1

        '''
        # check if s2l is activated
        if self.channel >= 0:
            current_volume = 3*float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            #self.speed = current_volume
        else:
            current_volume = self.speed
        # modulate brightness
        for x in range(10):
            world[:,x,:,:] *= np.sin(current_volume * (x - self.step))
        '''

        modulation_world = np.zeros([10, 10, 10])
        x = np.linspace(0,9,10)*self.wavelength
        y = np.linspace(0,9,10)*self.wavelength+self.spread
        z = np.linspace(0,9,10)*self.wavelength+self.spread**2

        modulation_world = np.sum(np.meshgrid(x,y,z), axis = 0)

        modulation_world = 0.5*np.sin(modulation_world*self.step*self.speed) + 0.5

        for i in range(3):
            world[i, :, :, :] = world[i, :, :, :] - modulation_world*self.amount


        # compressor for SHAPE
        # world[:,:,:,:] = np.clip(world[:,:,:,:],0,1)**self.shape

        self.step += 1

        return np.clip(world, 0, 1)
