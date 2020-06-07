# modules
import numpy as np
from scipy.signal import sawtooth
from generators.g_genhsphere import gen_hsphere
import pyaudio
import scipy
import struct
from random import randint
from scipy.fftpack import fft, fftfreq


class g_sound_lines():

    def __init__(self):

        # get initial random lines
        self.lines = []
        for i in range(10):
            self.lines.append([slice(0, 10, 1), randint(0, 9), randint(0, 9)])

        self.counter = 1
        self.reset = 20

        # parameters for normalization
        self.buffer = []
        self.normalized = False
        self.norm = [0, 1]
        self.norm_trigger_value = 0

        # sound2light stuff
        self.sample_rate = 44100
        self.buffer_size = int(44100/20)
        self.thres_factor = 0
        self.channel = 0

        p = pyaudio.PyAudio()

        self.stream = p.open(
            format = pyaudio.paInt16,	# paFloat32 vs paInt16 ?
            channels = 1,
            rate = self.sample_rate,
            input = True,
            output = False,
            frames_per_buffer = self.buffer_size
            )

    def return_values(self):
        return [b'sound_lines', b'reset', b'channel', b'normalize', b'']


    def __call__(self, args):

        total_volume = self.update_line()**2

        self.reset = args[0]*20+1
        self.channel = int(args[1]*len(total_volume)-1)

        # detect change at normalize parameter or channel
        if self.norm_trigger_value != args[2]:
            print('clearing buffer')
            # clear buffer and reset normalized switch
            self.buffer = []
            self.normalized = False
            self.norm_trigger_value = args[2]

        if not self.normalized :
            # fill buffer
            self.buffer.append(total_volume[self.channel])
            # self.buffer.append(total_volume[self.channel])

            # save min and max
            self.norm[0] = min(self.buffer)
            self.norm[1] = max(self.buffer)

            if len(self.buffer) > 50:
                self.normalized = True
                print('normalized:', self.norm)

        # apply normalization
        if self.norm[1] > self.norm[0]:
            # the ()**4 is important! otherwise, this is just bright or dark
            current_volume = ((total_volume[self.channel]-self.norm[0]) /(self.norm[1]-self.norm[0]))**4
            #print(current_volume, total_volume[self.channel], self.norm[0], self.norm[1])
        else:
            current_volume = total_volume[self.channel]

        # now we can world with the sound
        world = np.zeros([3, 10, 10, 10])

        # get lines
        for line, threshold in zip(self.lines, range(len(self.lines))):
            if current_volume > threshold/len(self.lines):
                world[0, line[0], line[1], line[2]] = current_volume

        # copy to other colors
        world[1:, :, :, :] = world[0, :, :, :]
        world[2:, :, :, :] = world[0, :, :, :]

        if self.counter > self.reset:
            self.lines = []
            # reset lines
            for i in range(10):
                self.lines.append([slice(0, 10, 1), randint(0, 9), randint(0, 9)])

            self.counter = 0

        self.counter += 1

        return np.round(np.clip(world, 0, 1), 3)

    def update_line(self):
        buf = self.stream.read(self.buffer_size)
        data = scipy.array(struct.unpack("%dh"%(self.buffer_size), buf))

        freqs, y = self.get_fft(data)

        # Normalize
        y = y / 5.0

        # Average into chunks of N
        N = 100

        yy = [scipy.average(y[n:n+N]) for n in range(0, len(y), N)]
        yy = yy[:int(len(yy)/2)] # Discard half of the samples, as they are mirrored

        # now do some threshold detection
        # for i in range(len(yy)):
        #    yy[i] = self.control_threshold(yy[i], self.threshold)

        return np.round(np.clip(yy,0,1),2)

    def control_threshold(self, dat, thres):
        if dat < thres:
            return 0.0
        else:
            return dat

    def get_fft(self, data):
        FFT = fft(data)                                # Returns an array of complex numbers
        freqs = fftfreq(self.buffer_size, 1.0/self.sample_rate)  # Returns an array containing the frequency values

        y = abs(FFT[0:int(len(FFT)/2)])/1000                # Get amplitude and scale
        y = scipy.log(y) - 2                           # Subtract noise floor (empirically determined)
        return (freqs, y)
