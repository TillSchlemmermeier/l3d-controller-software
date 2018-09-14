import numpy as np
import pyaudio
from scipy.fftpack import fft, fftfreq
import scipy
import struct

class e_s2l():
    def __init__(self):
        self.amount = 1.0
        # sound2light stuff
        self.sample_rate = 44100
        self.buffer_size = 2**11

        p = pyaudio.PyAudio()

        self.stream = p.open(
            format = pyaudio.paInt16,	# paFloat32 vs paInt16 ?
            channels = 1,
            rate = self.sample_rate,
            input = True,
            output = False,
            frames_per_buffer = self.buffer_size
        )
        self.thres_list = [0.4, 0.4, 0.4, 0.4, 0.8]


    def control(self, amount, blub1, blub2):
        self.amount = amount

    def label(self):
        return ['amount',round(self.amount,2),
                'empty','empty',
                'empty','empty']

    def generate(self, step, world):
        total_volume = self.update_line()
        world[0, :, :, :] *= total_volume[0]*self.amount
        world[1, :, :, :] *= total_volume[2]*self.amount
        world[2, :, :, :] *= total_volume[3]*self.amount
        return np.clip(world, 0, 1)

    def get_fft(self, data):
        FFT = fft(data)                                # Returns an array of complex numbers
        freqs = fftfreq(self.buffer_size, 1.0/self.sample_rate)  # Returns an array containing the frequency values

        y = abs(FFT[0:int(len(FFT)/2)])/1000                # Get amplitude and scale
        y = scipy.log(y) - 2                           # Subtract noise floor (empirically determined)
        return (freqs, y)

    def threshold(self, dat, thres):
        if dat < thres:
            return 0.0
        else:
            return dat

    def update_line(self):
        buf = self.stream.read(self.buffer_size)
        data = scipy.array(struct.unpack("%dh"%(self.buffer_size), buf))

        freqs, y = self.get_fft(data)

        # Normalize
        y = y / 5

        # Average into chunks of N
        N = 100
        yy = [scipy.average(y[n:n+N]) for n in range(0, len(y), N)]
        yy = yy[:int(len(yy)/2)] # Discard half of the samples, as they are mirrored

        # now do some threshold detection
        for i in range(4):
            yy[i] = self.threshold(yy[i], self.thres_list[i])


        return np.round(np.clip(yy,0,1),2)
