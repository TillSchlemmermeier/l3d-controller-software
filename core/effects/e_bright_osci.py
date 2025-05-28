# modules
import numpy as np
from multiprocessing import shared_memory

class e_bright_osci():
    '''
    Effect: oscillating brightness
    '''

    def __init__(self):
        self.speed = 1.0
        self.shape = 1.0
        self.step = 0
        self.amount = 1.0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 4

    def return_state(self):
        if self.channel >= 0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return [
            ['speed', 'speed', round(self.speed,2)],
            ['shape', 'shape', round(self.shape,2)],
            ['amount', 'amount', round(self.amount,2)],
            ['channel', 'channel', channel],
        ]

    def __call__(self, world, args):
        # parsing input
        self.speed   = args[0]*2-1
        self.shape   = args[1]*3+0.01
        self.channel = int(args[3]*4)-1
        self.amount  = args[2]

        # check if s2l is activated
        if self.channel >= 0:
            current_volume = 3*float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            #self.speed = current_volume
        else:
            current_volume = self.speed
        # modulate brightness
        for x in range(10):
            brightness = np.sin(current_volume * (x - self.step))*0.5 + 0.5
            world[:, x, :, :] *= np.clip((1 - self.amount*brightness),0,1)
            # world[:,x,:,:] *= (1 np.sin(current_volume * (x - self.step))

        # compressor for SHAPE
        world[:,:,:,:] = np.clip(world[:,:,:,:],0,1)**self.shape

        self.step += 1

        return np.clip(world, 0, 1)
