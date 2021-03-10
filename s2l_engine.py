import numpy as np
import pyaudio
from scipy.fftpack import fft, fftfreq
import scipy
import struct
from time import sleep, time

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.interpolate import griddata
from scipy.ndimage.filters import uniform_filter1d
import multiprocessing as mp
from multiprocessing import shared_memory
import matplotlib as mpl

from PyQt5 import QtCore

def sound_process(array):
    # initialize pyaudio
    sample_rate = 44100
    buffer_size = int(44100/20)
    p = pyaudio.PyAudio()
    sound_values = mp.shared_memory.SharedMemory(name = "global_s2l_memory")

    # find pule audio device
    chosen_device_index = -1
    for x in range(0,p.get_device_count()):
        info = p.get_device_info_by_index(x)
        print(info)
        if info["name"] == "pulse":
            chosen_device_index = info["index"]
            print("chosen index: ", chosen_device_index)

    stream = p.open(
        format = pyaudio.paInt16,
        channels = 1,
        rate = sample_rate,
        input_device_index = chosen_device_index,
        input = True,
        output = False,
        frames_per_buffer = buffer_size)

    freq_axis = 10000*np.linspace(0, 1, 60)**2

    # initialize selector
    selectors = [200, 1000, 2000, 5000]
    thresholds = [0.0, 0.0, 0.0, 0.0]

    # inital read
    dump = stream.read(1024)
    data = struct.unpack("%dh"%(1024), dump)
    FFT = fft(data)
    freqs = fftfreq(1024, 1.0/sample_rate)

    print('\nstarting sound loop\n')

    mpl.rcParams['toolbar'] = 'None'
    # initialize figure
    fig, ax = plt.subplots(figsize=(3.3, 1.9))#'''figsize=(4, 1.8)'''50
    fig.canvas.manager.window.move(348, 565)
    fig.canvas.manager.window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    fig.canvas.manager.window.setWindowOpacity(1.0)

    ax.set_xlim(50, 10000)
    ax.set_ylim(-0.1,2)
    line = ax.plot(freqs, np.abs(FFT))[0]
    select1 = ax.plot([100,100], [-10,10], label = '0', color = 'red')[0]
    select2 = ax.plot([100,500], [-10,10], label = '1', color = 'green')[0]
    select3 = ax.plot([100,1000], [-10,10], label = '2', color = 'blue')[0]
    select4 = ax.plot([100,2000], [-10,10], label = '3', color = 'orange')[0]

    thres1 = ax.plot([100-10,100+10], [0,0],  color = 'red')[0]
    thres2 = ax.plot([100-10,100+10], [0,0],  color = 'green')[0]
    thres3 = ax.plot([100-10,100+10], [0,0],  color = 'blue')[0]
    thres4 = ax.plot([100-10,100+10], [0,0], color = 'orange')[0]

    ax.set_xscale('symlog', linthreshx=0.01)

    ax.set_xticks([50, 100, 250, 500, 1000, 2500, 5000, 10000])
    ax.set_xticklabels([50, 100, 250, 500, 1000, 2500, 5000, 10000])
    plt.legend(loc='upper center',bbox_to_anchor=(0.5,1.2),ncol=4,fancybox=True)

    # normalization
    normalized = [False]
    buffer = []
    min = [np.zeros(60)]
    max = [np.ones(60)]

    norm_value = [0.0]
    last_value = [0.0]
    armed = [True]
    starttime = [time()]

    def update_line(frame, normalized, buffer, min, max):
        # update selectors
        selectors[0] = (array[10]**2)*10000
        selectors[1] = (array[11]**2)*10000
        selectors[2] = (array[12]**2)*10000
        selectors[3] = (array[13]**2)*10000

        # update threshold
        thresholds[0] = array[14]
        thresholds[1] = array[15]
        thresholds[2] = array[16]
        thresholds[3] = array[17]

        # check for normalizing
        if array[18] != norm_value[0]:
            normalized[0] = False
            norm_value[0] = array[18]
            buffer[:] = []
            print('s2l engine : reseting normalization')


        # read raw data and unpack it
        n_available = stream.get_read_available()
        dump = stream.read(buffer_size)
        data = struct.unpack("%dh"%(buffer_size), dump)

        # perform fourier transformation
        FFT = fft(data)
        freqs = fftfreq(buffer_size, 1.0/sample_rate)

        # smoothing and interpolating to correct axis
        FFT_smooth = uniform_filter1d(np.abs(FFT), size=10)
        final_data = griddata(freqs, FFT_smooth, freq_axis, method='cubic', fill_value=0)

        # normalize the whole thing
        if not normalized[0]:
            buffer.append(final_data)

            if len(buffer) > 100:
                print('normalized')
                normalized[0] = True
                min[0] = np.min(np.array(buffer), axis = 0)
                max[0] = np.max(np.array(buffer), axis = 0)


        final_data = (final_data - min[0])/(max[0] - min[0])

        # set data
        line.set_data(freq_axis, final_data)

        select1.set_data([selectors[0], selectors[0]], [-10,10])
        select2.set_data([selectors[1], selectors[1]], [-10,10])
        select3.set_data([selectors[2], selectors[2]], [-10,10])
        select4.set_data([selectors[3], selectors[3]], [-10,10])

        thres1.set_data([selectors[0]-0.1*selectors[0], selectors[0]+0.1*selectors[0]], [thresholds[0],thresholds[0]])
        thres2.set_data([selectors[1]-0.1*selectors[1], selectors[1]+0.1*selectors[1]], [thresholds[1],thresholds[1]])
        thres3.set_data([selectors[2]-0.1*selectors[2], selectors[2]+0.1*selectors[2]], [thresholds[2],thresholds[2]])
        thres4.set_data([selectors[3]-0.1*selectors[3], selectors[3]+0.1*selectors[3]], [thresholds[3],thresholds[3]])

        # write data
        for i in range(len(selectors)):
            # get data
            freq_ind = np.argmin(abs(freq_axis - selectors[i]))
            current_volume = round(final_data[freq_ind],4)

            # apply threshold
            if current_volume < thresholds[0]:
                current_volume = 0.0

            # apply gain
            current_volume *= (array[19]*4 + 1)
            #current_volume = current_volume**(1-array[19]*0.5)

            string = '{:8}'.format(current_volume)
            bla = bytearray('{:.8}'.format(string[:8]),'utf-8')
            sound_values.buf[i*8:i*8+8] =  bla

            if i == 0:
                if current_volume > 0.5 and armed[0]:
                    last_value[0] += 1
                    string = '{:8}'.format(last_value[0])
                    bla = bytearray('{:.8}'.format(string[:8]),'utf-8')
                    sound_values.buf[32:40] = bla
                    armed[0] = False
                    starttime[0] = time()
                elif current_volume < 0.5 and not armed[0] and time()-starttime[0] > 0.3:
                    armed[0] = True
                else:
                    pass

        return line, select1, select2, select3, select4, thres1, thres2, thres3, thres4

    animation = FuncAnimation(fig, func = update_line, interval=10, blit=True, fargs = (normalized, buffer, min, max))
    plt.show()
