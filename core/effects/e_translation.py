import numpy as np
from scipy.ndimage import shift
from multiprocessing import shared_memory
import struct
import time

class e_translation():
    def __init__(self):
        self.xspeed = 0.5
        self.yspeed = 0.5
        self.zspeed = 0.5
        self.step = 0
        self.edge = 'wrap'  # 'wrap', 'disappear' or 'projection'
        self.mode = 'loop'  # 'loop', 'fixed', 'trigger', 's2l'
        self.x_counter = 0
        self.y_counter = 0
        self.z_counter = 0

        self.x_shift = 0
        self.y_shift = 0
        self.z_shift = 0

        # For 'trigger' mode: track when trigger was activated and duration
        self.trigger_active = False
        self.trigger_start_time = 0
        self.trigger_duration = 0.25  # 0.25 seconds
        self.last_sound_value = 0

        self.sound_values = shared_memory.SharedMemory(name="global_s2l_memory")
        # trigger: current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))
        # s2l: current_volume = struct.unpack('d', bytes(self.sound_values.buf[0:8]))

        # Accumulators for 'projection' mode (only used when edge == 'projection')
        self.x_plus_accum = np.zeros((3, 10, 10))   # +X face (x=9)
        self.x_minus_accum = np.zeros((3, 10, 10))  # -X face (x=0)
        self.y_plus_accum = np.zeros((3, 10, 10))   # +Y face (y=9)
        self.y_minus_accum = np.zeros((3, 10, 10))  # -Y face (y=0)
        self.z_plus_accum = np.zeros((3, 10, 10))   # +Z face (z=9)
        self.z_minus_accum = np.zeros((3, 10, 10))  # -Z face (z=0)

    def return_state(self):
        return [
            ['X speed', 'xspeed', self.xspeed],
            ['Y speed', 'yspeed', self.yspeed],
            ['Z speed', 'zspeed', self.zspeed],
            ['edge', 'edge', self.edge],
            ['mode', 'mode', self.mode],
        ]

    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.xspeed = int((args[0] - 0.5) * 20)
        self.yspeed = int((args[1] - 0.5) * 20)
        self.zspeed = int((args[2] - 0.5) * 20)
        self.edge = ['wrap', 'disappear', 'projection'][round(args[3]*2)]
        self.mode = ['loop', 'fixed', 'trigger', 's2l'][round(args[4]*3)]
        # === PARAMETERS END ===

        # Mode-specific logic (sound data only unpacked when needed)
        if self.mode == 'loop':
            self.handle_loop_mode()
        elif self.mode == 'fixed':
            self.handle_fixed_mode()
        elif self.mode == 'trigger':
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]  # Trigger uses buf[32:40]
            self.handle_trigger_mode(current_volume)
        elif self.mode == 's2l':
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[0:8]))[0]    # S2L uses buf[0:8]
            self.handle_s2l_mode(current_volume)

        # Apply shift only if non-zero
        if self.x_shift != 0 or self.y_shift != 0 or self.z_shift != 0:
            self.apply_shift(world)

        self.step += 1
        np.clip(world, 0, 1, out=world)  # In-place clipping
        return world

    def handle_loop_mode(self):
        """Original looping behavior: counters accumulate and shifts change over time"""
        # Reset shift and accumulators if speed is 0 or shift exceeds bounds
        if self.xspeed == 0 or abs(self.x_shift) > 8:
            self.x_shift = 0
            if self.edge == 'projection':
                self.x_plus_accum.fill(0)
                self.x_minus_accum.fill(0)
        if self.yspeed == 0 or abs(self.y_shift) > 8:
            self.y_shift = 0
            if self.edge == 'projection':
                self.y_plus_accum.fill(0)
                self.y_minus_accum.fill(0)
        if self.zspeed == 0 or abs(self.z_shift) > 8:
            self.z_shift = 0
            if self.edge == 'projection':
                self.z_plus_accum.fill(0)
                self.z_minus_accum.fill(0)

        # X axis shift logic
        if self.xspeed != 0:
            self.x_counter += abs(self.xspeed)
            if self.x_counter >= 10:
                self.x_shift += 1 if self.xspeed > 0 else -1
                self.x_counter -= 10

        # Y axis shift logic
        if self.yspeed != 0:
            self.y_counter += abs(self.yspeed)
            if self.y_counter >= 10:
                self.y_shift += 1 if self.yspeed > 0 else -1
                self.y_counter -= 10

        # Z axis shift logic
        if self.zspeed != 0:
            self.z_counter += abs(self.zspeed)
            if self.z_counter >= 10:
                self.z_shift += 1 if self.zspeed > 0 else -1
                self.z_counter -= 10

    def handle_fixed_mode(self):
        """Fixed mode: shift is constant based on speed values, no animation"""
        self.x_shift = self.xspeed
        self.y_shift = self.yspeed
        self.z_shift = self.zspeed
        # Accumulators not used in fixed mode unless projection, but reset only if needed
        if self.edge != 'projection':
            self.reset_accumulators()

    def handle_trigger_mode(self, current_volume):
        """Trigger mode: shift only during sound peak events"""
        # Check if sound value increased (peak detected)
        if current_volume > self.last_sound_value:
            self.trigger_active = True
            self.trigger_start_time = time.time()

        self.last_sound_value = current_volume
        # Check if trigger duration has elapsed
        if self.trigger_active:
            elapsed_time = time.time() - self.trigger_start_time
            if elapsed_time >= self.trigger_duration:
                self.trigger_active = False
                # Reset shifts when trigger ends
                self.x_shift = 0
                self.y_shift = 0
                self.z_shift = 0
                self.x_counter = 0
                self.y_counter = 0
                self.z_counter = 0
                if self.edge == 'projection':
                    self.reset_accumulators()
            else:
                # During trigger duration, apply loop logic
                self.update_trigger_shifts()
        else:
            # Not triggered, no shift
            self.x_shift = 0
            self.y_shift = 0
            self.z_shift = 0

    def update_trigger_shifts(self):
        """Update shifts during trigger active period using loop-like logic"""
        # X axis shift logic
        if self.xspeed != 0:
            self.x_counter += abs(self.xspeed)
            if self.x_counter >= 10:
                self.x_shift += 1 if self.xspeed > 0 else -1
                self.x_counter -= 10

        # Y axis shift logic
        if self.yspeed != 0:
            self.y_counter += abs(self.yspeed)
            if self.y_counter >= 10:
                self.y_shift += 1 if self.yspeed > 0 else -1
                self.y_counter -= 10

        # Z axis shift logic
        if self.zspeed != 0:
            self.z_counter += abs(self.zspeed)
            if self.z_counter >= 10:
                self.z_shift += 1 if self.zspeed > 0 else -1
                self.z_counter -= 10

    def handle_s2l_mode(self, current_volume):
        """S2L mode: shift scales with sound level based on speed values"""
        # Scale the shift based on sound value (0.0 to 1.0 range typically)
        current_volume = np.clip(current_volume, 0.0, 1.0)

        # Apply sound scaling to shifts
        self.x_shift = int(self.xspeed * current_volume)
        self.y_shift = int(self.yspeed * current_volume)
        self.z_shift = int(self.zspeed * current_volume)

        # Accumulators not used in s2l mode unless projection
        if self.edge != 'projection':
            self.reset_accumulators()

    def reset_accumulators(self):
        """Reset all accumulators (only call when needed)"""
        self.x_plus_accum.fill(0)
        self.x_minus_accum.fill(0)
        self.y_plus_accum.fill(0)
        self.y_minus_accum.fill(0)
        self.z_plus_accum.fill(0)
        self.z_minus_accum.fill(0)

    def apply_shift(self, world):
        """Apply the calculated shift to the world using the current edge"""
        shift_vector = (self.x_shift, self.y_shift, self.z_shift)  # Cache for reuse

        if self.edge == 'wrap':
            for i in range(3):
                world[i, :, :, :] = shift(world[i, :, :, :], shift=shift_vector, order=0, mode='wrap')
        elif self.edge == 'disappear':
            for i in range(3):
                world[i, :, :, :] = shift(world[i, :, :, :], shift=shift_vector, order=0, mode='constant', cval=0.0)
        elif self.edge == 'projection':
            # Accumulate outgoing values only if shifting in that direction
            if self.x_shift > 0:
                self.x_plus_accum += world[:, 9, :, :]
            elif self.x_shift < 0:
                self.x_minus_accum += world[:, 0, :, :]
            if self.y_shift > 0:
                self.y_plus_accum += world[:, :, 9, :]
            elif self.y_shift < 0:
                self.y_minus_accum += world[:, :, 0, :]
            if self.z_shift > 0:
                self.z_plus_accum += world[:, :, :, 9]
            elif self.z_shift < 0:
                self.z_minus_accum += world[:, :, :, 0]

            # Apply shift
            for i in range(3):
                world[i, :, :, :] = shift(world[i, :, :, :], shift=shift_vector, order=0, mode='constant', cval=0.0)

            # Set faces to accumulated projections
            if self.x_shift > 0:
                world[:, 9, :, :] = self.x_plus_accum
            elif self.x_shift < 0:
                world[:, 0, :, :] = self.x_minus_accum
            if self.y_shift > 0:
                world[:, :, 9, :] = self.y_plus_accum
            elif self.y_shift < 0:
                world[:, :, 0, :] = self.y_minus_accum
            if self.z_shift > 0:
                world[:, :, :, 9] = self.z_plus_accum
            elif self.z_shift < 0:
                world[:, :, :, 0] = self.z_minus_accum