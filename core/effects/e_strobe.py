from multiprocessing import shared_memory
import numpy as np
import struct

class e_strobe():
    '''
    Effect: strobe with waveforms and sound trigger
    
    Parameters:
    - channel: -1 (off), 0-3 (frequency bands), 4 (trigger)
    - duration: how long the flash lasts
    - interval: time between flashes
    - waveform: 'rect', 'ramp', 'down', 'triangle'
    - invert: bool, inverts the strobe effect (only for sound channels)
    - iterations: number of flashes on trigger (only for channel 4)
    '''

    def __init__(self):
        self.duration = 1
        self.interval = 1
        self.waveform = 'rect'
        self.channel = -1
        self.sound_values = shared_memory.SharedMemory(name="global_s2l_memory")
        self.counter = 0
        self.lastvalue = 0
        self.invert = False
        self.iterations = 1
        self.trigger_count = 0

    def return_state(self):
        return [
            ['channel', 'channel', self.channel],
            ['duration', 'duration', round(self.duration, 1)],
            ['interval', 'interval', round(self.interval, 1)],
            ['waveform', 'waveform', self.waveform],
            ['s2l invert', 'invert', str(self.invert)],
            ['# on trigger', 'iterations', self.iterations],
        ]

    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.channel = ['Off', 0, 1, 2, 3, 'Trigger'][round(args[0] * 5)]
        self.duration = int(args[1] * 11) + 1
        self.interval = int(args[2] * 11) + 1
        self.waveform = ['rect', 'ramp', 'down', 'triangle'][round(args[3] * 3)]
        self.invert = args[4] > 0.5
        self.iterations = int(args[5] * 10) + 1
        # === PARAMETERS END ===

        cycle_length = self.duration + self.interval
        position = self.counter % cycle_length
        should_flash = False

        # Manual mode: always flash
        if self.channel == 'Off':
            should_flash = True

        # Trigger mode
        elif self.channel == 'Trigger':
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            if current_volume > self.lastvalue:
                self.trigger_count = 0
                self.lastvalue = current_volume
            
            should_flash = self.trigger_count < self.iterations
            if position == cycle_length - 1:
                self.trigger_count += 1

        # Frequency bands
        else:
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0] ** 4
            should_flash = current_volume > 0.5

        if should_flash:
            in_on_phase = position < self.duration
            
            # XOR logic: flash when (in_on_phase and not invert) OR (not in_on_phase and invert)
            if in_on_phase ^ self.invert:
                world = self._apply_waveform(world, position if in_on_phase else (position - self.duration), self.duration if in_on_phase else self.interval)
            else:
                world[:, :, :, :] = 0
            
        else:
            # No flash: black if not inverted, bright if inverted
            if not self.invert:
                world[:, :, :, :] = 0

        self.counter += 1
        return np.clip(world, 0, 1)

    def _apply_waveform(self, world, position, on):
        progress = position / max(1, on)
        
        if self.waveform == 'rect':
            intensity = 1.0
        elif self.waveform == 'ramp':
            intensity = progress
        elif self.waveform == 'down':
            intensity = 1.0 - progress
        elif self.waveform == 'triangle':
            intensity = 1.0 - abs(2 * progress - 1)
        
        world[:, :, :, :] *= intensity
        return world