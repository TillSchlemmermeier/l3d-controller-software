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
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 4

    #strings for GUI
    def return_values(self):
        return [b'bright_osci', b'speed', b'shape', b'', b'channel']

    def return_gui_values(self):
        if self.channel >= 0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.speed,2)), str(round(self.shape,2)), '', channel), 'utf-8')

    def __call__(self, world, args):
        # parsing input
        self.speed = args[0]*2-1
        self.shape = args[1]*3+0.001
        self.channel = int(args[3]*4)-1

        # check if s2l is activated
        if self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            self.speed = current_volume

        # modulate brightness
        for x in range(10):
            world[:,x,:,:] *= np.sin(self.speed*self.step+x)

        # compressor for SHAPE
        world[:,:,:,:] = np.clip(world[:,:,:,:],0,1)**self.shape

        self.step += 1

        return np.clip(world, 0, 1)
