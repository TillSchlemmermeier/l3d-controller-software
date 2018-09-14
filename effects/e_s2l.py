import numpy as np
import pyaudio
from scipy.fftpack import fft, fftfreq
import scipy


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
            frames_per_buffer = self.butter_size
        )


    def control(self, amount, blub1, blub2):
        self.amount = amount

    def label(self):
        return ['amount',round(self.amount,2),
                'empty','empty',
                'empty','empty']

    def generate(self, step, world):
        total_volume = self.update_line()
        world[0, :, :, :] *= total_volume[0]
        world[1, :, :, :] *= total_volume[1]
        world[2, :, :, :] *= total_volume[2]
        return np.clip(world, 0, 1)

    def get_fft(self, data):
        FFT = fft(data)                                # Returns an array of complex numbers
        freqs = fftfreq(self.buffer_size, 1.0/self.sample_rate)  # Returns an array containing the frequency values

        y = abs(FFT[0:len(FFT)/2])/1000                # Get amplitude and scale
        y = scipy.log(y) - 2                           # Subtract noise floor (empirically determined)
        return (freqs, y)

    def update_line(self):
        buf = stream.read(self.buffer_size)
        data = scipy.array(struct.unpack("%dh"%(self.buffer_size), buf))

        freqs, y = self.get_fft(data, self.buffer_size, self.sample_rate)

        # Normalize
        y = y / 5

        # Average into chunks of N
        N = 50
        yy = [scipy.average(y[n:n+N]) for n in range(0, len(y), N)]
        yy = yy[:int(len(yy)/2)] # Discard half of the samples, as they are mirrored

        return yy
