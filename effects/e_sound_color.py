# modules
import numpy as np
from colorsys import rgb_to_hsv, hsv_to_rgb
from random import random, uniform
import pyaudio
from scipy.fftpack import fft, fftfreq
import scipy
import struct

class e_sound_color():
    '''
    '''

    def __init__(self):

        self.max = 0.5
        self.min = 0.5

        self.c1 = 0.0
        self.distance = 0.0

        self.amount = 1

        self.sample_rate = 44100
        self.buffer_size = 2**10
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


    def control(self, amount, threshold, channel):
        self.amount = amount
        self.threshold = threshold
        self.channel = int(channel*4)

#        self.thres_list = self.thres_list*self.thres_factor
        # new_list = [x+1 for x in my_list]
#        self.thres_list = [x+self.thres_factor for x in self.thres_list]

    def label(self):
        return ['amount',round(self.amount,2),
                'threshold',round(self.threshold,2),
                'channel',round(self.channel)]

    def generate(self, step, world):

        color_ind = self.update_line()

        color = hsv_to_rgb(np.clip(color_ind[self.channel]*self.amount, 0, 1), 1.0, 1.0)

        '''
        if color_ind[self.channel] > self.max:
            self.max = color_ind[self.channel]

        if color_ind[self.channel] < self.min:
            self.min = color_ind[self.channel]

        if step % 20 == 0:
            print(self.min, self.max)
        '''

        world[0,:,:,:] *= color[0]
        world[1,:,:,:] *= color[1]
        world[2,:,:,:] *= color[2]

        return np.clip(world,0,1)

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
        for i in range(len(yy)):
            yy[i] = self.control_threshold(yy[i], self.threshold)

        return np.round(np.clip(yy,0,1),2)
