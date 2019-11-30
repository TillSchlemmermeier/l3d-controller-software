import numpy as np
import pyaudio
from scipy.fftpack import fft, fftfreq
import scipy
from scipy.signal import gaussian as Gaussian
import struct
from itertools import cycle

class e_s2l_shiftcolor():
    def __init__(self):
        self.amount = 1.0
        # sound2light stuff
        self.sample_rate = 44100
        self.buffer_size = 882
        self.thres_factor = 0
        self.freqs = range(0,int(self.sample_rate/2+1),int(self.sample_rate/self.buffer_size))
        self.channel = 100
        self.gaussian = Gaussian(21,10)
        self.gaussian[0] = 0.0
        self.gaussian[-1] = 0.0
        self.colors = cycle([[1.0, 0.0, 0.0],
                       [1.0, 0.5, 0.0],
                       [1.0, 1.0, 0.0],
                       [0.5, 1.0, 0.0],
                       [0.0, 1.0, 0.0],
                       [0.5, 1.0, 0.0],
                       [1.0, 1.0, 0.0],
                       [1.0, 0.5, 0.0]
                       ])


        self.color = next(self.colors)
        p = pyaudio.PyAudio()

#        print('2')

        self.stream = p.open(
            format = pyaudio.paInt16,	# paFloat32 vs paInt16 ?
            channels = 1,
            rate = self.sample_rate,
            input = True,
            output = False,
            frames_per_buffer = self.buffer_size
            )
        self.threshold = 0.5


    def control(self, amount, threshold, channel):
        self.amount = amount
        self.threshold = threshold
        self.channel = int(channel*10)+1

    def label(self):
        return ['amount',round(self.amount,2),
                'threshold',round(self.threshold,2),
                'channel',round(self.channel)]

    def generate(self, step, world):
        total_volume = self.update_line()
        if step % 10 == 0:
            print(total_volume[100])
        # check for change
        if total_volume[100]*self.amount >= 0.5:
            self.color = next(self.colors)

        # make colorful!
        world[0, :, :, :] *= self.color[0]
        world[1, :, :, :] *= self.color[1]
        world[2, :, :, :] *= self.color[2]
        return np.clip(world, 0, 1)

    def get_fft(self, data):
        FFT = fft(data)                                # Returns an array of complex numbers
        freqs = fftfreq(self.buffer_size, 1.0/self.sample_rate)  # Returns an array containing the frequency values

        y = abs(FFT[0:int(len(FFT)/2)])/1000                # Get amplitude and scale
        y = scipy.log(y) - 2                           # Subtract noise floor (empirically determined)
        return (freqs, y)

    def control_threshold(self, dat, thres):
        if dat < thres:
            return 0.0
        else:
            return dat

    def update_line(self):

        data = np.fft.rfft(np.fromstring(
            self.stream.read(self.buffer_size), dtype=np.float32)
        )
        print(np.mean(data))

        data = np.log10(np.sqrt(
            np.real(data)**2+np.imag(data)**2) / self.buffer_size) * 10

#        gdata = np.convolve(data, self.gaussian, mode = 'same')

        return np.round(np.clip(data,0,1),2)
