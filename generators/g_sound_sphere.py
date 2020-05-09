# modules
import numpy as np
from scipy.signal import sawtooth
from generators.g_genhsphere import gen_hsphere
import pyaudio
import scipy
import struct
from scipy.fftpack import fft, fftfreq
# fortran routine is in g_growing_sphere_f.f90

class g_sound_sphere():

    def __init__(self):
        self.maxsize = 10
        self.growspeed = 1
        self.oscillate = 0

        self.amount = 1.0
        # sound2light stuff
        self.sample_rate = 44100
        self.buffer_size = 2**11
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


    #Strings for GUI
    def return_values(self):
        return [b'sound_sphere', b'amount', b'threshold', b'oscillate', b'']

    def __call__(self, args):
        self.amount = args[0]*10
        self.threshold = args[1]
        self.oscillate = args[2]

        world = np.zeros([3, 10, 10, 10])

        size = self.update_line()**2*self.amount

        # creates hollow sphere with parameters
        world[0, :, :, :] = gen_hsphere(size, 5.5,5.5,5.5)
        world[1:, :, :, :] = world[0, :, :, :]
        world[2:, :, :, :] = world[0, :, :, :]

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
