import numpy as np
import pyaudio
from scipy.fftpack import fft, fftfreq
import scipy
import matplotlib.pyplot as plt
import struct

class e_s2l():
    def __init__(self):
        self.amount = 1.0
        # sound2light stuff
        self.sample_rate = 44100
        self.buffer_size = 2**10
        self.thres_factor = 0
        self.channel = 1

        #pa = pyaudio.PyAudio()
        '''
        chosen_device_index = 0
        for x in range(0,pa.get_device_count()):
            info = pa.get_device_info_by_index(x)
            print(pa.get_device_info_by_index(x))
            if info["name"] == "pulse":
                chosen_device_index = info["index"]
                print("Chosen index: ", chosen_device_index)

        print('1.5')
        '''

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
        self.amount = amount*2
        self.threshold = threshold
        self.channel = int(channel*10)

#        self.thres_list = self.thres_list*self.thres_factor
        # new_list = [x+1 for x in my_list]
#        self.thres_list = [x+self.thres_factor for x in self.thres_list]

    def label(self):
        return ['amount',round(self.amount,2),
                'threshold',round(self.threshold,2),
                'channel',round(self.channel)]

    def generate(self, step, world):
        total_volume = self.update_line()
        world[0, :, :, :] *= total_volume[self.channel]*self.amount
        world[1, :, :, :] *= total_volume[self.channel]*self.amount
        world[2, :, :, :] *= total_volume[self.channel]*self.amount
        return np.clip(world, 0, 1)

    def get_fft(self, data):
        FFT = fft(data)                                # Returns an array of complex numbers
        freqs = fftfreq(self.buffer_size, 1.0/self.sample_rate)  # Returns an array containing the frequency values

        y = abs(FFT[0:int(len(FFT)/2)])/1000                # Get amplitude and scale
        y = scipy.log(y) - 2                           # Subtract noise floor (empirically determined)
        plt.figure(1)
        plt.plot(freqs, y)
        plt.show()
        return (freqs, y)

    def control_threshold(self, dat, thres):
        if dat < thres:
            return 0.0
        else:
            return dat

    def update_line(self):

        buf = self.stream.read(self.buffer_size)
        data = scipy.array(struct.unpack("%dh"%(self.buffer_size), buf))
        print(np.fft.rfft(data[])


        data = np.fft.rfft(np.fromstring(
            self.stream.read(self.buffer_size), dtype=np.int16)
        )

        print(data[0])
        data = np.abs(data)
        #data = np.log10(np.sqrt(
        #    np.real(data)**2+np.imag(data)**2) / self.buffer_size) * 10

        # plt.figure(1)
        # plt.plot(data)
        # plt.show()

        #print(data)
#        print(data)
        data += 100

#        data *= 0.01

        binsize = 5
        newdata = np.zeros(binsize)

        step = int(500/binsize)
#        print(data[step*5])
        newdata[0] = np.mean(data[10:step])
        newdata[1] = np.mean(data[1*step:2*step])
        newdata[2] = np.mean(data[2*step:3*step])
        newdata[3] = np.mean(data[3*step:4*step])
        newdata[4] = np.mean(data[4*step:5*step])

        newdata *= 0.001
        newdata -= 0.2
        #print(np.clip(np.round(newdata,2),0,1))

#        print(np.shape(data))
        #yy = [scipy.average(data[n:n+N]) for n in range(0, len(data), N)]
#        print(np.shape(yy))
        #yy = np.clip(np.round(yy,2)-0.9,0,1)
        #yy = yy**2
        #print(newdata)
#        yy = yy[:int(len(yy)/2)] # Discard half of the samples, as they are mirrored

        # now do some threshold detection
        #for i in range(len(yy)):
        #    yy[i] = self.control_threshold(yy[i], self.threshold)

        #print(yy)
        return np.clip(np.round(newdata,2),0,1)
