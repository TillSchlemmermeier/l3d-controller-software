
import numpy as np
import pyaudio
from scipy.fftpack import fft, fftfreq
import scipy
import struct
from time import sleep
from colorsys import rgb_to_hsv, hsv_to_rgb

class e_sound_color():
    def __init__(self):
        # initialize pyaudio
        self.sample_rate = 44100
        self.buffer_size = int(44100/20) # 20 is best
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
        self.threshold = 0.5
        self.channel = 10
        self.colorstep = 0.1
        self.color = 0.0

    def return_values(self):
        # strings for GUI
        return [b's2l', b'color step', b'threshold', b'channel', b'normalize switch']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.colorstep,1)), str(round(self.threshold,1)), str(self.channel), '') ,'utf-8')

    def __call__(self, world, args):
        # get sound data
        total_volume = self.update_line()

        # process parameters
        self.colorstep = args[0]+0.001
        self.threshold = args[1]# +0.001
        self.channel = int(args[2]*len(total_volume)-1)

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
        else:
            current_volume = total_volume[self.channel]

        # apply threshold
        if current_volume > self.threshold:
            self.color += self.colorstep

        color = hsv_to_rgb(self.color, 1, 1)
        world[0, :, :, :] *= color[0]
        world[1, :, :, :] *= color[1]
        world[2, :, :, :] *= color[2]

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

        #print(self.stream.get_read_available())

        temp_buf = self.stream.read(100,exception_on_overflow = False)
#        print('-')

        while True:
#            print('')
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
