import struct
import numpy as np
from multiprocessing import shared_memory

class e_s2l():

    def __init__(self):
        self.amount = 1.0
        self.channel = 1.0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.lastvalue = 0
        self.counter = 0
        self.step = 8
        self.mode = 'normal'
        self.decay = 0
        self.value = 0.0

    def return_state(self):
        return [
            ['amount', 'amount', round(self.amount,1)],
            ['channel', 'channel', self.channel],
            ['mode', 'mode', self.mode],
            ['decay', 'decay', round(self.decay,1)],
        ]
    
    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.amount = args[0]
        self.channel = [0, 1, 2, 3, 'Trigger', 'Trigger/2'][round(args[1]*5)]
        self.mode = ['normal', 'invert'][round(args[2])]
        self.decay = round(args[3]*0.5,2)
        # === PARAMETERS END ===


        # modulate brightness with audio
        if isinstance(self.channel, int):

            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]**4

            if self.decay == 0:
                world[:, :, :, :] *= (1-self.amount) + np.clip(current_volume,0,1)*self.amount
            else:
                if current_volume > self.value:
                    self.value = current_volume
                elif self.value == 0:
                    world[:, :, :, :] *= 0
                else:
                    self.value = np.clip(self.value * (1-self.decay), 0, 1)
                    world[:, :, :, :] *= (1-self.amount) + self.value*self.amount

        else:
            # trigger normal
            if self.channel == 'Trigger':
                current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
                if current_volume > self.lastvalue:
                    self.lastvalue = current_volume
                    self.counter = 0

            # trigger half
            elif self.channel == 'Trigger/2':

                current_volume = struct.unpack('d', bytes(self.sound_values.buf[40:48]))[0]
                if current_volume == 1:
                   self.lastvalue = current_volume
                   self.counter = 0

                # current_volume = float(str(self.sound_values.buf[72:80],'utf-8'))
                #print(current_volume)
                world[:, :, :, :] *= (1-self.amount) + np.clip(current_volume,0,1)*self.amount


            if self.mode == 'normal':

                # old stuff
                if self.counter < self.step:
                    world[:, :, :, :] *= (1 - self.amount) + ((self.step - self.counter) / self.step) * self.amount
            else:
                # if self.counter < 20:
                #     pass
                if 15 < self.counter: # < (self.step + 1000)
#                    print(self.counter ,(self.counter-15)/(self.step + 100))
                    world[:, :, :, :] *= ((self.counter-15)/(self.step + 100))
                #elif self.counter > (self.step + 100):
                #    world[:, :, :, :] = 0.0
                else:
                    world[:, :, :, :] = 0.0
            self.counter += 1


        return np.clip(world, 0, 1)
