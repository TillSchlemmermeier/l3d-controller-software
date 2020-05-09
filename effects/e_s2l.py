
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
        self.buffer_size = 3000
        self.thres_factor = 0
        self.channel = 1

        p = pyaudio.PyAudio()

        self.stream = p.open(
            format = pyaudio.paInt16,	# paFloat32 vs paInt16 ?
            channels = 1,
            rate = self.sample_rate,
            input = True,
            output = False,
            frames_per_buffer = self.buffer_size
            )

        self.threshold = 0.5


    #strings for GUI
    def return_values(self):
        return [b's2l', b'amount', b'channel', b'threshold', b'']

    def __call__(self, world, args):
        total_volume = self.update_line()
        # print(len(total_volume))

        self.amount = args[0]
        self.channel = int(args[1]*len(total_volume)-1)
        self.threshold = args[2]

        world[0, :, :, :] *= total_volume[self.channel]*self.amount
        world[1, :, :, :] *= total_volume[self.channel]*self.amount
        world[2, :, :, :] *= total_volume[self.channel]*self.amount
        return np.clip(world, 0, 1)

    def get_fft(self, data):
        FFT = fft(data)
        # Returns an array of complex numbers
        freqs = fftfreq(self.buffer_size, 1.0/self.sample_rate)

        y = abs(FFT[0:int(len(FFT)/2)])/1000                # Get amplitude and scale
        y = scipy.log(y) - 2
        # Subtract noise floor (empirically determined)
        return (freqs, y)

    def control_threshold(self, dat, thres):
        if dat < thres:
            return 0.0
        else:
            return dat

    def update_line(self):
        buf = self.stream.read(self.buffer_size)
        data = scipy.array(struct.unpack("%dh"%(self.buffer_size), buf))

        freqs, y = self.get_fft(data)

        # Normalize
        # y = y / 5.0

        # Average into chunks of N
        N = 10

        yy = [scipy.average(y[n:n+N]) for n in range(0, len(y), N)]
        yy = yy[:int(len(yy)/2)] # Discard half of the samples, as they are mirrored

        # now do some threshold detection
        for i in range(len(yy)):
            yy[i] = self.control_threshold(yy[i], self.threshold)

        return np.round(np.clip(yy, 0, 1), 4)
