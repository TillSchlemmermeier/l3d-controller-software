
import numpy as np
import pyaudio
from scipy.fftpack import fft, fftfreq
import scipy
import struct
from time import sleep
from generators.g_genhsphere import gen_hsphere


class g_soundsphere():
    def __init__(self):
        # initialize pyaudio
        self.sample_rate = 44100
        self.buffer_size = int(44100/20)
        p = pyaudio.PyAudio()

        self.stream = p.open(
            format = pyaudio.paInt16,	# paFloat32 vs paInt16 ?
            channels = 1,
            rate = self.sample_rate,
            input = True,
            output = False,
            frames_per_buffer = self.buffer_size,
#            timeout = 0.001
            )

        # parameters for normalization
        self.buffer = []
        self.normalized = False
        self.norm = [0, 1]
        self.norm_trigger_value = 0

        # parameters
        self.amount = 1.0
        self.channel = 10
        self.maxsize = 5
        self.smooth = 0.25

        self.last_value = 0

    def return_values(self):
        # strings for GUI
        return [b'SoundSphere', b'maxsize', b'channel', b'smooth', b'normalize switch']


    def __call__(self, args):
        # get sound data
        total_volume = self.update_line()

        # process parameters
        self.maxsize = args[0]*10
        self.smooth = args[2] * 0.5
        self.channel = int(args[1]*len(total_volume)-1)

        # detect change at normalize parameter or channel
        if self.norm_trigger_value != args[3]:
            print('clearing buffer')
            # clear buffer and reset normalized switch
            self.buffer = []
            self.normalized = False
            self.norm_trigger_value = args[3]


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

        # mix with old value
        current_volume = (1-self.smooth) * current_volume + self.smooth * self.last_value

        size = self.maxsize*current_volume

        world = np.zeros([3, 10, 10, 10])

        world[0, :, :, :] = gen_hsphere(size, 4.5, 4.5, 4.5)
        world[1:, :, :, :] = world[0, :, :, :]
        world[2:, :, :, :] = world[0, :, :, :]

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

        temp_buf = self.stream.read(100)

        while True:
            # read buffer and calculate spectrum
            temp_buf += self.stream.read(self.stream.get_read_available())
            if len(temp_buf) > self.buffer_size*2:
                break

        buf = temp_buf[-self.buffer_size*2:]
#        print(self.buffer_size, len(temp_buf), len(buf))

        data = scipy.array(struct.unpack("%dh"%(self.buffer_size), buf))

        freqs, y = self.get_fft(data)

        # print(len(buf))

        # Average into chunks of N
        #N = 10
        #yy = [scipy.average(y[n:n+N]) for n in range(0, len(y), N)]
        #yy = yy[:int(len(yy)/2)] # Discard half of the samples, as they are mirrored

        yy = y
        #print(yy)

        # now do some threshold detection
        # for i in range(len(yy)):
        #     yy[i] = self.control_threshold(yy[i], self.threshold)

        return np.round(yy, 2)


'''
    def control_threshold(self, dat, thres):
        if dat < thres:
            return 0.0
        else:
            return dat

'''
