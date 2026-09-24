import os
import sys
import numpy as np
import pyaudio
import socket
import json
import multiprocessing as mp
from scipy.fftpack import fft, fftfreq
from scipy.ndimage.filters import uniform_filter1d
from time import time
from collections import deque
import struct

class BeatDetector:
    '''
    Onset detection on the low band.

    A beat is a sudden rise in energy, so this watches the frame to frame
    increase (the spectral flux) rather than the level.
    '''

    HISTORY = 3.0       # seconds of flux behind the moving bar
    K = 2.2             # how far above the recent median an onset has to sit
    LEVEL_GATE = 0.5    # normalised low band under which nothing counts
    REFRACTORY = 0.30   # seconds before the next beat can be called

    def __init__(self, hops_per_window, hops_per_second):
        # deque: a list that is fast to add to and remove from at both ends.
        self.previous = deque(maxlen=hops_per_window)
        self.history = deque(maxlen=round(self.HISTORY*hops_per_second))
        self.last_beat = 0.0
        self.beats = 0

    def __call__(self, band, level, now):
        '''take the magnitudes of the low band and its normalised level,
        return True on a beat'''
        # compress first. the rise from a kick is then the same size whether the
        # track is mastered loud or quiet
        band = np.log1p(band)

        if len(self.previous) < self.previous.maxlen:
            self.previous.append(band)
            return False

        # only the rises. a note ending is not an onset
        flux = float(np.sum(np.maximum(band - self.previous[0], 0)))
        self.previous.append(band)

        self.history.append(flux)

        bar = np.median(self.history)*self.K

        fired = (level >= self.LEVEL_GATE
                 and flux > bar
                 and now - self.last_beat > self.REFRACTORY)
        if fired:
            self.last_beat = now
            self.beats += 1

        return fired


def sound_process(state):
    
    # initialize pyaudio
    sample_rate = 44100
    buffer_size = int(44100/20)
    # audio ─────────────────────────────────────────────────▶ time
    #          0 ms                  50 ms                   100 ms
    # frame 1  [=======================]
    # frame 2          [=======================]
    # frame 3                  [=======================]
    # frame 4                          [=======================]
    #          |hop    |hop    |hop    |
    hops_per_window = 3
    hop = buffer_size//hops_per_window

    # Suppress stderr output from PyAudio initialization
    devnull = os.open(os.devnull, os.O_WRONLY) # open /dev/null
    original_stderr_fd = os.dup(sys.stderr.fileno()) # Save original stderr fd
    os.dup2(devnull, sys.stderr.fileno()) # Redirect stderr to /dev/null
    p = pyaudio.PyAudio() # Initialize PyAudio
    os.dup2(original_stderr_fd, sys.stderr.fileno()) # Restore original stderr fd
    os.close(original_stderr_fd) # Close the duplicated fd
    os.close(devnull) # Close /dev/null fd

    sound_values = mp.shared_memory.SharedMemory(name = "global_s2l_memory")

    # find pipewire audio device (Nachfolger von pulseaudio)
    pulse_device_index = -1
    for x in range(0,p.get_device_count()):
        info = p.get_device_info_by_index(x)
        if info["name"] == "pipewire":
            pulse_device_index = info["index"]
            print("chosen audio device: ")
            print(info)

    if pulse_device_index == -1:
        print("\nWarning: No pipewire device found, using default input device")
        pulse_device_index = p.get_default_input_device_info()['index']
        print("chosen audio device: ")
        print(p.get_device_info_by_index(pulse_device_index))


    stream = p.open(
        format = pyaudio.paInt16,
        channels = 1,
        rate = sample_rate,
        input_device_index = pulse_device_index,
        input = True,
        output = False,
        frames_per_buffer = hop)

    # initialize frequency axis for spectrum
    freq_axis = np.logspace(0, 5, 60)

    # initialize frequency selector
    selectors = [200, 1000, 2000, 5000] # frequency
    thresholds = [0.0, 0.0, 0.0, 0.0]   # threshold

    print('\nstarting sound loop\n')

    reference = [np.zeros(60)]  # one reference per bin, roughly the loudest it has been lately
    reference_rise = 1 - 0.9**(1/hops_per_window)       # climbs a tenth of the way to a new peak every 50 ms
    reference_ceiling = 1.05**(1/hops_per_window)       # but never more than this much of itself
    reference_fall = 0.9995**(1/hops_per_window)        # and about 4 dB a minute back down

    # the reference only gives way while music is actually playing. Read off the
    # balance between the bass and the rest of the spectrum: turning the volume
    # down scales every bin alike and leaves the balance where it was, a break
    # does not. Too high a number here and a quiet set stops re-scaling by itself;
    # too low and a long break drags the scale down with it
    bass_share = 8.0

    # trigger
    norm_value = 0.0
    last_value = 0.0
    detector = BeatDetector(hops_per_window, sample_rate/hop)
    samples = np.frombuffer(stream.read(buffer_size), dtype=np.int16)

    # the bins a kick lives in. the raw fft axis, not the log one used for the
    # display, and taken before the smoothing that would flatten the transient.
    freqs = fftfreq(buffer_size, 1.0/sample_rate)
    kick_band = (freqs >= 40) & (freqs <= 110)
    # the same window on the display axis, where the normalisation has run
    level_band = (freq_axis >= 40) & (freq_axis <= 110)
    # what the bass is weighed against to tell music from an ambient passage
    mid_band = (freqs >= 300) & (freqs <= 4000)

    # create LFOs

    lfo = [0.0, 0.0, 0.0, 0.0]

    # === SETUP UDP SOCKET ===
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_dest = ("127.0.0.1", 8001)


    def update():
        nonlocal norm_value
        nonlocal last_value
        nonlocal samples

        # everything this frame needs from the state
        with state.lock:
            needs_update = state['s2l_update']
            resetting = state['s2l_normalize']
            auto_normalize = state['s2l_auto_normalize']
            gain = state['s2l_gain']
            if needs_update:
                new_selectors = list(state['s2l_values'])
                new_thresholds = list(state['s2l_thresholds'])
                state['s2l_update'] = False
            if resetting:
                state['s2l_normalize'] = False

        if needs_update:
            for i in range(len(selectors)):
                selectors[i] = (new_selectors[i]**2)*10000
                thresholds[i] = new_thresholds[i]

        # check for normalizing
        if resetting:
            reference[0][:] = 0
            print('s2l engine : reseting normalization')

        # the newest hop pushes the oldest out of the window
        samples = np.concatenate((samples[hop:], np.frombuffer(stream.read(hop), dtype=np.int16)))

        # perform fourier transformation
        FFT   = fft(samples)
        magnitude = np.abs(FFT)

        # smoothing and interpolating to correct axis
        FFT_smooth = uniform_filter1d(magnitude, size=10)
        # 1-D interpolation onto the log frequency axis
        pos = freqs >= 0
        final_data = np.interp(freq_axis, freqs[pos], FFT_smooth[pos], right=0)

        if not reference[0].any():          # first frame, or after a reset
            reference[0] = final_data.copy()

        # with the automatic rescaling off the reference still follows a peak
        # up, it just never gives way again
        playing = (auto_normalize
                   and magnitude[kick_band].mean() > bass_share*magnitude[mid_band].mean())

        target = reference[0] + (final_data - reference[0])*reference_rise
        reference[0] = np.where(final_data > reference[0],
                                np.minimum(target, reference[0]*reference_ceiling),
                                reference[0]*(reference_fall if playing else 1.0))

        final_data = final_data/(reference[0] + 1e-9)

        # beat detection
        beat = detector(magnitude[kick_band],
                        float(np.mean(final_data[level_band])), time())
        
        current_volumes = []

        for i in range(len(selectors)):
            # get data for this frequency
            freq_ind = np.argmin(abs(freq_axis - selectors[i]))
            current_volume = round(final_data[freq_ind],4)

            # apply threshold
            if current_volume < thresholds[i]:
                current_volume = 0.0

            # apply gain
            current_volume *= (gain*4 + 1)

            current_volumes.append(current_volume)

        # read from shared memory to get eventual changes from oneshot
        last_value = struct.unpack('d', sound_values.buf[32:40])[0]
        if beat:
            last_value += 1.0

        # Add trigger values
        current_volumes.append(last_value)

        # Add trigger2 values
        if last_value % 2 == 0:
            current_volumes.append(last_value)
        else:
            current_volumes.append(last_value - 1)

        # write the processed sound value for this frequency to shared memory
        sound_values.buf[0:48] = struct.pack('6d', *current_volumes)

        # send data to frontend
        data = {
            "type": "spectrum_data",
            "data": {
                "spectrum": final_data.tolist(),
                "trigger": last_value,
            }
        }

        udp_sock.sendto(json.dumps(data).encode('utf-8'), udp_dest)

    # stream.read() waits for the next hop
    while True:
        update()