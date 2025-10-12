import numpy as np
from scipy.ndimage import shift

class e_translation():

    def __init__(self):
        self.xspeed = 0
        self.yspeed = 0
        self.zspeed = 0
        self.step = 0
        self.mode = 'wrap'  # 'wrap', 'disappear' or 'projection'
        self.x_counter = 0
        self.y_counter = 0
        self.z_counter = 0

        self.x_shift = 0
        self.y_shift = 0
        self.z_shift = 0

        # Accumulators for 'projection' mode
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
            ['mode', 'mode', self.mode],
        ]

    def __call__(self, world, args):
        self.xspeed = int((args[0] - 0.5) * 20)
        self.yspeed = int((args[1] - 0.5) * 20)
        self.zspeed = int((args[2] - 0.5) * 20)
        self.mode = ['wrap', 'disappear', 'projection'][int(round(args[3]*2))]

        # Reset shift and accumulators if speed is 0 or shift exceeds bounds
        if self.xspeed == 0 or abs(self.x_shift) > 8:
            self.x_shift = 0
            self.x_plus_accum.fill(0)
            self.x_minus_accum.fill(0)
        if self.yspeed == 0 or abs(self.y_shift) > 8:
            self.y_shift = 0
            self.y_plus_accum.fill(0)
            self.y_minus_accum.fill(0)
        if self.zspeed == 0 or abs(self.z_shift) > 8:
            self.z_shift = 0
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

        # Apply accumulated shift every frame
        if self.x_shift != 0 or self.y_shift != 0 or self.z_shift != 0:
            if self.mode == 'wrap':
                # Wrap mode: pixels wrap around edges
                for i in range(3):
                    world[i, :, :, :] = shift(
                        world[i, :, :, :],
                        shift=[self.x_shift, self.y_shift, self.z_shift],
                        order=0,  # Nearest neighbor for pixel-perfect shifts
                        mode='wrap'
                    )
            elif self.mode == 'disappear':
                # Disappear mode: pixels vanish at edges
                for i in range(3):
                    world[i, :, :, :] = shift(
                        world[i, :, :, :],
                        shift=[self.x_shift, self.y_shift, self.z_shift],
                        order=0,
                        mode='constant',
                        cval=0.0
                    )

            elif self.mode == 'projection':
                # Projection mode: accumulate outgoing values on the pushed-out faces
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
                
                # Apply shift with constant fill (0.0)
                for i in range(3):
                    world[i, :, :, :] = shift(
                        world[i, :, :, :],
                        shift=[self.x_shift, self.y_shift, self.z_shift],
                        order=0,
                        mode='constant',
                        cval=0.0
                    )
                
                # Set the faces to the accumulated projections
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

        self.step += 1

        return np.clip(world, 0, 1)