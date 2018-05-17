import numpy as np
import pyaudio


class e_s2l():
    '''
    '''
    def __init__(self):
        self.amount = 1.0
        # sound2light stuff
        RATE = 44100
        self.BUFFER = 882

        p = pyaudio.PyAudio()

        self.stream = p.open(
            format = pyaudio.paFloat32,
            channels = 1,
            rate = RATE,
            input = True,
            output = False,
            frames_per_buffer = self.BUFFER
        )


    def control(self, amount ,blub1, blub2):
        self.amount = amount

    def label(self):
        return ['empty','empty','empty','empty','empty','empty']

    def generate(self, step, world):

        total_volume = self.update_line()

        world[:,:,:,:] *= self.amount *total_volume

        return np.clip(world, 0, 1)

    def update_line(self):
        try:
            # take FFT of data from buffer
            # buffer size is a critical parameter, i think
            data = np.fft.rfft(np.fromstring(
                self.stream.read(self.BUFFER), dtype=np.float32)
                )

            data2 = np.log10(np.sqrt(
                np.real(data)**2+np.imag(data)**2) / self.BUFFER) * 10

            value = np.mean(-data2[:20])
        except IOError:
            value = 1.0


        return np.clip(value-20.0,0,50)
