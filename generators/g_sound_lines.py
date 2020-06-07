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
            direction = randint(0, 2)
            if direction == 0:
                self.lines.append([slice(0, 10, 1), randint(0, 9), randint(0, 9)])
            elif direction == 1:
                self.lines.append([:, randint(0, 9), slice(0, 10, 1), randint(0, 9)])
            elif direction == 2:
                self.lines.append([:, randint(0, 9), randint(0, 9), slice(0, 10, 1)])

        self.amount = 1.0
        self.counter = 1
        self.reset = 20

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
        self.threshold = 0.5


    def return_values(self):
        return [b'sound_lines', b'reset', b'threshold', b'', b'']


    def __call__(self, args):
        self.reset = args[0]*20+1
        self.threshold = args[1]
        self.oscillate = args[2]

        world = np.zeros([3, 10, 10, 10])

        brightness = self.update_line()**2*self.amount

        # get lines
        for line, threshold in zip(self.lines, range(len(self.lines))/len(self.lines)):
            if size > threshold:
                world[0, line[0], line[1], line[2]] = brightness

        # copy to other colors
        world[1:, :, :, :] = world[0, :, :, :]
        world[2:, :, :, :] = world[0, :, :, :]

        if self.counter > self.reset:
        self.lines = []
            # reset lines
            for i in range(10):
                direction = randint(0, 2)
                if direction == 0:
                    self.lines.append([slice(0, 10, 1), randint(0, 9), randint(0, 9)])
                elif direction == 1:
                    self.lines.append([:, randint(0, 9), slice(0, 10, 1), randint(0, 9)])
                elif direction == 2:
                    self.lines.append([:, randint(0, 9), randint(0, 9), slice(0, 10, 1)])

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
        for i in range(len(yy)):
            yy[i] = self.control_threshold(yy[i], self.threshold)

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
