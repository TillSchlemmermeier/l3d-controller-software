from multiprocessing import shared_memory

class e_soundstrobo():


    def __init__(self):
        # parameters
        self.amount = 1.0
        self.channel = 1.0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.counter = 0

    def return_values(self):
        # strings for GUI
        return [b's2l', b'amount', b'channel', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.amount,1)), str(self.channel), '','') ,'utf-8')

    def __call__(self, world, args):
        # process parameters
        self.amount = args[0]
        self.channel = int(args[1]*3)
        current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))**4

        # apply manipulation
        if current_volume > 0.5
            if self.counter == 0:
                world[:, :, :, :] = 0
                self.counter += 1
            else:
                self.counter = 0
                
        return np.clip(world, 0, 1)
