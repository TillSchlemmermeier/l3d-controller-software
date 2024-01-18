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
#from PyQt5 import QtCore, QtGui

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl

def sound_process(array):

    # initialize pyaudio
    sample_rate = 44100
    buffer_size = int(44100/20)
    print("\n \n \nInitializing PyAudio...")
    p = pyaudio.PyAudio()
    print("End of PyAudio initialization \n----------------------------- \n \n")
    sound_values = mp.shared_memory.SharedMemory(name = "global_s2l_memory")

    # find pulse audio device
    pulse_device_index = -1
    for x in range(0,p.get_device_count()):
        info = p.get_device_info_by_index(x)
        if info["name"] == "pulse":
            pulse_device_index = info["index"]
            print("chosen audio device: ")
            print(info)

    stream = p.open(
        format = pyaudio.paInt16,
        channels = 1,
        rate = sample_rate,
        input_device_index = pulse_device_index,
        input = True,
        output = False,
        frames_per_buffer = buffer_size)

    # initialize frequency axis for spectrum
    freq_axis = np.logspace(0, 5, 60)

    # initialize frequency selector
    selectors = [200, 1000, 2000, 5000] # frequency
    thresholds = [0.0, 0.0, 0.0, 0.0]   # threshold

    # inital reading of spectrum
    dump = stream.read(1024)
    data = struct.unpack("%dh"%(1024), dump)
    FFT = fft(data)
    freqs = fftfreq(1024, 1.0/sample_rate)

    print('\nstarting sound loop\n')

    # initialize matplotlib figure
    # for spectrum visualizer

    mpl.rcParams['toolbar'] = 'None'

    fig, ax = plt.subplots()#figsize=(10.6, 6.5)
    plt.xticks(fontsize = 12, rotation = 0)
    plt.yticks(fontsize = 12)
    ax.set_facecolor('black')
    fig.set_facecolor('black')
    ax.xaxis.label.set_color('red')
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')

    fig.canvas.manager.window.setGeometry(1921, 1200, 600, 424)
    fig.canvas.manager.window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    fig.canvas.manager.window.setWindowOpacity(1.0)

    ax.set_xlim(50, 10000)
    ax.set_ylim(-0.1,2)
    line = ax.plot(freqs, np.abs(FFT), color='white', lw=3)[0]
    select1 = ax.plot([100,100], [-10,10], label = '0', color = 'red', linewidth = 5)[0]
    select2 = ax.plot([100,500], [-10,10], label = '1', color = 'green', linewidth = 5)[0]
    select3 = ax.plot([100,1000], [-10,10], label = '2', color = 'blue', linewidth = 5)[0]
    select4 = ax.plot([100,2000], [-10,10], label = '3', color = 'orange', linewidth = 5)[0]

    thres1 = ax.plot([100-10,100+10], [0,0],  color = 'red', linewidth = 6)[0]
    thres2 = ax.plot([100-10,100+10], [0,0],  color = 'green', linewidth = 6)[0]
    thres3 = ax.plot([100-10,100+10], [0,0],  color = 'blue', linewidth = 6)[0]
    thres4 = ax.plot([100-10,100+10], [0,0], color = 'orange', linewidth = 6)[0]

    ax.set_xscale('symlog', linthresh=0.01)

    ax.set_xticks([50, 100, 250, 500, 1000, 2500, 5000, 10000])
    ax.set_xticklabels([50, 100, 250, 500, 1000, 2500, 5000, 10000])
    plt.legend(loc='upper center',bbox_to_anchor=(0.5,1.16),ncol=4,fancybox=True, fontsize=12, labelcolor='white', facecolor='black')

    # normalization
    normalized = [False]
    buffer = []
    min = [np.zeros(60)]
    max = [np.ones(60)]

    # trigger
    norm_value = [0.0]
    last_value = [0.0]
    armed = [True]
    starttime = [time()]
    trigger_counter = 0

    def update_line(frame, normalized, buffer, min, max):
        '''
        function for update the plotting window, which also
        calls the functions to read the spectrum and parse it

        this function uses `array`, which is passed from the parent
        function to the function `sound_process`. that's the
        global parameters array
        '''
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

        # normalize the whole thing if normalizing was set
        # to "not normalized"
        if not normalized[0]:
            buffer.append(final_data)

            if len(buffer) > 60:
                print('normalized')
                normalized[0] = True
                min[0] = np.min(np.array(buffer), axis = 0)
                max[0] = np.max(np.array(buffer), axis = 0)

        # final data is the final processed spectrum
        final_data = (final_data - min[0])/(max[0] - min[0] + 0.001)

        # set data for plot
        line.set_data(freq_axis, final_data)

        select1.set_data([selectors[0], selectors[0]], [-10,10])
        select2.set_data([selectors[1], selectors[1]], [-10,10])
        select3.set_data([selectors[2], selectors[2]], [-10,10])
        select4.set_data([selectors[3], selectors[3]], [-10,10])

        thres1.set_data([selectors[0]-0.1*selectors[0], selectors[0]+0.1*selectors[0]], [thresholds[0],thresholds[0]])
        thres2.set_data([selectors[1]-0.1*selectors[1], selectors[1]+0.1*selectors[1]], [thresholds[1],thresholds[1]])
        thres3.set_data([selectors[2]-0.1*selectors[2], selectors[2]+0.1*selectors[2]], [thresholds[2],thresholds[2]])
        thres4.set_data([selectors[3]-0.1*selectors[3], selectors[3]+0.1*selectors[3]], [thresholds[3],thresholds[3]])

        # this loop writes the current intensities for the
        # different chosen frequencies to global array
        for i in range(len(selectors)):
            # get data for this frequency
            freq_ind = np.argmin(abs(freq_axis - selectors[i]))
            current_volume = round(final_data[freq_ind],4)

            # apply threshold
            if current_volume < thresholds[0]:
                current_volume = 0.0

            # apply gain, which can be controlled from
            # a single poti from the midimix
            current_volume *= (array[19]*4 + 1)

            # write the processed sound signal for this
            # frequency to sound_values
            string = '{:8}'.format(current_volume)
            bla = bytearray('{:.8}'.format(string[:8]),'utf-8')
            sound_values.buf[i*8:i*8+8] =  bla

            # process trigger
            # i is checking for the lowest frequency
            if i == 0:
                # if loud enough and armed is true
                # last_value is increased by 1
                if current_volume > 0.5 and armed[0]:
                    last_value[0] += 1
                    string = '{:8}'.format(last_value[0])
                    bla = bytearray('{:.8}'.format(string[:8]),'utf-8')
                    sound_values.buf[32:40] = bla

                    # trigger / 2
                    if last_value[0] % 2 == 0:
                        string = '{:8}'.format(last_value[0])
                        bla = bytearray('{:.8}'.format(string[:8]),'utf-8')
                        sound_values.buf[40:48] = bla

                    armed[0] = False
                    starttime[0] = time()
                elif current_volume < 0.5 and not armed[0] and time()-starttime[0] > 0.3:
                    armed[0] = True
                else:
                    pass

        # scatterplot.setData(color = np.clip(colors, 0, 1))

        return line, select1, select2, select3, select4, thres1, thres2, thres3, thres4

    '''
    t = QtCore.QTimer()
    t.timeout.connect(update)
    t.start(50)
    QtGui.QApplication.instance().exec_()

    '''
    animation = FuncAnimation(fig, func = update_line, interval=10, blit=True, fargs = (normalized, buffer, min, max))
    plt.show()
