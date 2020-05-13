
import numpy as np
import pyaudio
from scipy.fftpack import fft, fftfreq
import scipy
import struct


class e_s2l():
    def __init__(self):
        # initialize pyaudio
        self.sample_rate = 44100
        self.buffer_size = 2940
        p = pyaudio.PyAudio()

        self.stream = p.open(
            format = pyaudio.paInt16,	# paFloat32 vs paInt16 ?
            channels = 1,
            rate = self.sample_rate,
            input = True,
            output = False,
            frames_per_buffer = self.buffer_size
            )

        # parameters for normalization
        self.buffer = []
        self.normalized = False
        self.norm = [0, 1]
        self.norm_trigger_value = 0

        # parameters
        self.amount = 1.0
        self.channel = 10
        self.threshold = 0.5


    def return_values(self):
        # strings for GUI
        return [b's2l', b'amount', b'threshold', b'channel', b'normalize switch']


    def __call__(self, world, args):
        # get sound data
        total_volume = self.update_line()

        # process parameters
        self.amount = args[0]
        self.threshold = args[1]
        self.channel = int(args[1]*len(total_volume)-1)

        # detect change at normalize parameter or channel
        if self.norm_trigger_value != args[3]:
            # clear buffer and reset normalized switch
            self.buffer = []
            self.normalized = False


        if not self.normalized :
            # fill buffer
            self.buffer.append(total_volume[self.channel])
            # self.buffer.append(total_volume[self.channel])

            # save min and max
            self.norm[0] = min(self.buffer)
            self.norm[1] = max(self.buffer)

            if len(self.buffer) > 200:
                self.normalized = True

        # apply normalization
        current_volume = (total_volume[self.channel]-self.norm[0])/(self.norm[1]-self.norm[0])

        # apply threshold
        if current_volume < self.threshold:
            current_volume = 0

        # apply manipulation
        for i in range(3):
            world[i, :, :, :] *= (1-self.amount) + current_volume*self.amount

        return np.clip(world, 0, 1)


    def get_fft(self, data):
        FFT = fft(data)
        # Returns an array of complex numbers
        freqs = fftfreq(self.buffer_size, 1.0/self.sample_rate)

        # Get amplitude and scale
        y = abs(FFT[0:int(len(FFT)/2)])/1000
        y = scipy.log(y) - 2
        # Subtract noise floor (empirically determined)
        return (freqs, y)


    def update_line(self):
        # read buffer and calculate spectrum
        buf = self.stream.read(self.buffer_size)
        data = scipy.array(struct.unpack("%dh"%(self.buffer_size), buf))
        freqs, y = self.get_fft(data)

        # Average into chunks of N
        # N = 10
        # yy = [scipy.average(y[n:n+N]) for n in range(0, len(y), N)]
        # yy = yy[:int(len(yy)/2)] # Discard half of the samples, as they are mirrored

        yy = y

        # now do some threshold detection
        # for i in range(len(yy)):
        #     yy[i] = self.control_threshold(yy[i], self.threshold)

        return np.round(np.clip(yy, 0, 1), 4)


'''
    def control_threshold(self, dat, thres):
        if dat < thres:
            return 0.0
        else:
            return dat

'''
