# modules
import numpy as np
import pyaudio
from random import choice, random, randint
from scipy.fftpack import fft, fftfreq
import scipy
import struct


class g_soundsnake():
    def __init__(self):
        self.amount = 1.0
        # sound2light stuff
        self.sample_rate = 44100
        self.buffer_size = 2**11
        self.thres_factor = 0
        self.channel = 1

        pa = pyaudio.PyAudio()
        chosen_device_index = -1
        for x in range(0,pa.get_device_count()):
            info = pa.get_device_info_by_index(x)
            if info["name"] == "pulse":
                chosen_device_index = info["index"]

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

        self.counter = 0
        self.pos = [randint(0, 9), randint(0, 9), randint(0, 9)]
        self.axis = 0
        self.direction = 1
        self.frames = 20

        self.oldworld = np.zeros([3, 10, 10, 10])

    def control(self, amount, threshold, channel):
        self.amount = amount*10
        self.threshold = threshold*2
        self.channel = 3
        self.frames = int(channel*20)

    def label(self):
        return ['amount', round(self.amount,2),
                'threshold', round(self.threshold,2),
                'frames', round(self.frames)]

    def generate(self, step, world):
        world = np.zeros([3, 10, 10, 10])

        sound = self.amount*self.update_line()[self.channel]
        if sound > self.threshold:
            self.oldworld[:, :, :, :] = 0.0
            self.counter = self.frames

        if self.counter > 0:
            world[:, self.pos[0], self.pos[1], self.pos[2]] = 1.0

            if self.frames == 20:
                world += self.oldworld
                self.oldworld = world
                self.counter -= 1

            # move
            self.pos[self.axis] += self.direction
            if random() > 0.3:
                self.axis = choice([0, 1, 2])
                self.direction = choice([-1, 1])

            self.counter -= 1

            if self.pos[0] > 9:
                self.pos[0] = 0
            if self.pos[0] < 0:
                self.pos[0] = 9
            if self.pos[1] > 9:
                self.pos[1] = 0
            if self.pos[1] < 0:
                self.pos[1] = 9
            if self.pos[2] > 9:
                self.pos[2] = 0
            if self.pos[2] < 0:
                self.pos[2] = 9

        else:
            self.oldworld[:, :, :, :] = 0.0
            self.pos = [randint(0,9 ), randint(0,9 ), randint(0,9 )]

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
