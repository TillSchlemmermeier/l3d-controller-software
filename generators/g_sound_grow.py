# modules
import numpy as np
from generators.gen_central_glow_f import gen_central_glow
import pyaudio
from scipy.fftpack import fft, fftfreq
import scipy
import struct
from generators.g_genhsphere import gen_hsphere

class g_sound_grow():
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
        self.size = 1
        self.state = 0

    def control(self, amount, threshold, channel):
        self.amount = amount*15
        self.threshold = threshold
        self.channel = int(channel*6)

    def label(self):
        return ['amount',round(self.amount,2),
                'threshold',round(self.threshold,2),
                'channel',round(self.channel)]

    def generate(self, step, world):
        tempworld = np.zeros([10, 10, 10])

        size = self.amount*(1+self.update_line()[self.channel]-self.threshold)
        size = round(np.clip(size, 0, 10),2)

        if size > 2 and self.state == 0:
            self.state = 0.5
        elif self.state > 10:
            self.state = 0
        elif self.state > 0 and self.state <=10:
            self.state += 0.75
            world[0, :, :, :] = gen_hsphere(self.state, 4.5, 4.5, 4.5)
            world[1, :, :, :] = world[0, :, :, :]
            world[2, :, :, :] = world[0, :, :, :]
        else:
            pass

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
