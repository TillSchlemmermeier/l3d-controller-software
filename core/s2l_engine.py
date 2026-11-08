import numpy as np
import socket
import json
import multiprocessing as mp
from time import time
from collections import deque
import struct
import sounddevice as sd

class BeatDetector:
    '''
    Onset detection on the low band.

    A beat is a sudden rise in energy, so this watches the frame to frame
    increase (the spectral flux) rather than the level.
    '''

    HISTORY = 6.0       # seconds of flux behind the moving bar
    K = 2.2             # how far above the recent median an onset has to sit
    LEVEL_GATE = 0.5    # normalised kick band a beat needs, see sound_process. Also in SoundSpectrum.vue
    REFRACTORY = 0.30   # seconds before the next beat can be called

    def __init__(self, hops_per_window, hops_per_second):
        # deque: a list that is fast to add to and remove from at both ends. Starts
        # as zeros, so there is always a frame a window back
        self.previous = deque([0]*hops_per_window, maxlen=hops_per_window)
        self.history = deque(maxlen=round(self.HISTORY*hops_per_second))
        self.last_beat = 0.0

    def __call__(self, band, level, now, groove):
        '''take the magnitudes of the low band, its normalised level and
        whether the groove is on, return True on a beat'''
        # compress first. the rise from a kick is then the same size whether the
        # track is mastered loud or quiet
        band = np.log1p(band)

        # only the rises. a note ending is not an onset
        flux = float(np.sum(np.maximum(band - self.previous[0], 0)))
        self.previous.append(band)

        # the bar learns in the groove only, like the spectrum's scale.
        # It does fill up at start, and means nothing until it has
        if groove or len(self.history) < self.history.maxlen:
            self.history.append(flux)

        fired = (len(self.history) == self.history.maxlen
                 and level >= self.LEVEL_GATE
                 and flux > np.median(self.history)*self.K
                 and now - self.last_beat > self.REFRACTORY)
        if fired:
            self.last_beat = now

        return fired


def sound_process(state):

    sample_rate = 44100
    buffer_size = sample_rate//20
    # audio ─────────────────────────────────────────────────▶ time
    #          0 ms                  50 ms                   100 ms
    # frame 1  [=======================]
    # frame 2          [=======================]
    # frame 3                  [=======================]
    # frame 4                          [=======================]
    #          |hop    |hop    |hop    |
    hops_per_window = 3
    hop = buffer_size//hops_per_window

    sound_values = mp.shared_memory.SharedMemory(name = "global_s2l_memory")

    # find pipewire audio device (Nachfolger von pulseaudio)
    device = sd.query_devices("pipewire", kind="input")
    print("chosen audio device: ", device)

    stream = sd.InputStream(
        samplerate = sample_rate,
        channels = 1,
        dtype = "int16",
        device = device["index"],
        blocksize = hop)
    stream.start()

    # the display axis: 60 bins from 30 Hz to 16 kHz, log spaced.
    freq_axis = np.logspace(np.log10(30), np.log10(16000), 60)

    print('\nstarting sound loop\n')

    # each bin is scaled by the 99th percentile of its own last 15 s: about the
    # loudest it got, ignoring the top 1% so one stray frame doesn't set the scale.
    history = deque(maxlen=round(15*sample_rate/hop))
    reference = np.ones(60)
    # the first second goes in regardless, so there is a scale to start from
    first_frames = round(sample_rate/hop)

    # after that the history only takes frames in the groove: until 2 s after
    # the last beat. A break keeps the scale of the groove before it
    groove_hold = 2.0
    beat_time = -groove_hold

    detector = BeatDetector(hops_per_window, sample_rate/hop)
    samples = stream.read(buffer_size)[0][:, 0]

    # the bins a kick lives in. the raw fft axis, not the log one used for the
    # display, and taken before the smoothing that would flatten the transient.
    freqs = np.fft.rfftfreq(buffer_size, 1.0/sample_rate)
    kick_band = (freqs >= 40) & (freqs <= 110)
    # the same band on the display axis. A beat also needs its normalised level
    # at LEVEL_GATE, which keeps the quieter toms and rolls in a break out
    level_band = (freq_axis >= 40) & (freq_axis <= 110)

    # the spectrum gets a Hann window (i.e. each chunk is multiplied by a
    # gaussian-shaped curve), so a kick starting inside the window doesn't spill
    # over every frequency bin. The beat detector keeps the unwindowed fft it was tuned on
    window = np.hanning(buffer_size)
    # each display bin averages the fft bins between it and its neighbours. Below
    # about 180 Hz a display bin is narrower than the 20 Hz fft bins and takes the
    # interpolated value instead
    edges = np.sqrt(freq_axis[1:]*freq_axis[:-1])
    edges = np.concatenate(([freq_axis[0]**2/edges[0]], edges, [freq_axis[-1]**2/edges[-1]]))
    lo = np.searchsorted(freqs, edges[:-1]) # lower FFT bin index for each display bin
    hi = np.searchsorted(freqs, edges[1:])  # upper FFT bin index for each display bin
    wide = hi - lo >= 2                     # bins that hold at least two FFT bins

    # === SETUP UDP SOCKET ===
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_dest = ("127.0.0.1", 8001)

    # stream.read() waits for the next hop
    while True:
        # everything this frame needs from the state
        with state.lock:
            resetting = state['s2l_normalize']
            auto_normalize = state['s2l_auto_normalize']
            gain = state['s2l_gain']
            selectors = [(v**2)*10000 for v in state['s2l_values']]
            thresholds = list(state['s2l_thresholds'])
            if resetting:
                state['s2l_normalize'] = False

        # check for normalizing
        if resetting:
            history.clear()
            print('s2l engine : reseting normalization')

        # the newest hop pushes the oldest out of the window
        samples = np.concatenate((samples[hop:], stream.read(hop)[0][:, 0]))

        # perform fourier transformation
        magnitude = np.abs(np.fft.rfft(samples))
        spectrum = np.abs(np.fft.rfft(samples*window))

        # onto the log frequency axis. narrow bins: the value at the bin's frequency
        raw = np.interp(freq_axis, freqs, spectrum)
        # wide bins: the mean of the fft bins they cover
        for i in np.flatnonzero(wide):
            raw[i] = spectrum[lo[i]:hi[i]].mean()

        # scaled by the history so far; this frame joins it below
        final_data = raw/(reference + 1e-9)

        # beat detection
        now = time()
        groove = now - beat_time < groove_hold
        beat = detector(magnitude[kick_band], float(final_data[level_band].mean()), now, groove)
        if beat:
            beat_time = now
            groove = True

        # with the automatic rescaling off the scale stays where the first
        # second after a reset put it
        if (auto_normalize and groove) or len(history) < first_frames:
            history.append(raw)
            reference = np.percentile(history, 99, axis=0)

        current_volumes = []

        for i in range(len(selectors)):
            # get data for this frequency
            nearest_bin = np.argmin(abs(freq_axis - selectors[i]))

            # apply thresholds
            current_volume = max(final_data[nearest_bin] - thresholds[i], 0)/max(1 - thresholds[i], 0.1)

            # apply gain
            current_volume *= (gain*2 + 1)

            current_volumes.append(current_volume)

        # read from shared memory to get eventual changes from oneshot
        last_value = struct.unpack('d', sound_values.buf[32:40])[0]
        if beat:
            last_value += 1.0

        # the beat counter, trigger2 (counter on every 2nd beat), and whether a groove is playing
        current_volumes += [last_value, last_value - last_value % 2, float(groove)]

        # write the processed sound value for this frequency to shared memory
        sound_values.buf[0:56] = struct.pack('7d', *current_volumes)

        # send data to frontend
        data = {
            "type": "spectrum_data",
            "data": {
                "spectrum": final_data.tolist(),
                "trigger": last_value,
                "groove": groove
            }
        }

        udp_sock.sendto(json.dumps(data).encode('utf-8'), udp_dest)
