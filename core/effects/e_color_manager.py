import numpy as np
import struct
from multiprocessing import shared_memory

class e_color_manager():
    def __init__(self):
        self.gradient = []
        self.gradient_type = 'linear'
        self.speed = 0.5
        self.section_start = 0
        self.section_width = 100
        self.counter = 0
        self.rotate_speed_y = 0.0
        self.rotate_speed_z = 0.0
        self.rotation_counter = 0.0
        self.sound_to_light_options = []
        self.channel = 0
        self.current_volume = 0.5

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

        # Store base values (without sound modulation)
        self._base_speed = 0.5
        self._base_section_start = 0
        self._base_section_width = 100
        self._base_rotate_speed_y = 0.0
        self._base_rotate_speed_z = 0.0
        self._base_gradient = []

        # Pre-computed arrays for performance
        self._x_coords = None
        self._y_coords = None
        self._z_coords = None
        self._distance_cache = None
        self._colormap_cache = None
        self._gradient_hash = None
        self._inv_100 = 0.01

        # Pre-compute coordinate meshgrids for rotation
        self._coords_x = None
        self._coords_y = None
        self._coords_z = None

    def _precompute_coordinates(self):
        """Pre-compute coordinate arrays for vectorized operations"""
        # Store coordinates for all three axes
        self._x_coords = np.linspace(0, 1, 10)
        self._y_coords = np.linspace(0, 1, 10)
        self._z_coords = np.linspace(0, 1, 10)

        # Pre-compute 3D meshgrids for rotation (centered at origin)
        x, y, z = np.meshgrid(
            np.linspace(-0.5, 0.5, 10),
            np.linspace(-0.5, 0.5, 10),
            np.linspace(-0.5, 0.5, 10),
            indexing='ij'
        )
        self._coords_x = x
        self._coords_y = y
        self._coords_z = z
        
        # Pre-compute 3D distance array for radial gradients
        center = 4.5
        x, y, z = np.meshgrid(np.arange(10), np.arange(10), np.arange(10), indexing='ij')
        distances = np.sqrt((x - center)**2 + (y - center)**2 + (z - center)**2)
        
        # Cache different normalizations
        max_distance = np.sqrt(3 * (center ** 2))
        self._distance_cache = np.clip(distances / max_distance, 0, 1)


    def _rotate_coordinates(self, angle_y, angle_z):
        """
        Rotate the 3D coordinate system around Y and Z axes
        Returns the rotated X coordinates (gradient flows along X after rotation)
        """
        # Rotation around Y axis (yaw)
        cos_y = np.cos(angle_y)
        sin_y = np.sin(angle_y)
        x_rot_y = self._coords_x * cos_y - self._coords_z * sin_y
        z_rot_y = self._coords_x * sin_y + self._coords_z * cos_y
        y_rot_y = self._coords_y
        
        # Rotation around Z axis (pitch)
        cos_z = np.cos(angle_z)
        sin_z = np.sin(angle_z)
        x_final = x_rot_y * cos_z - y_rot_y * sin_z
        # y_final and z_final not needed for gradient calculation
        
        # Normalize to 0-1 range and return
        return (x_final + 0.5)  # Shift from [-0.5, 0.5] to [0, 1]


    def _create_fast_colormap(self, gradient):
        """Create a fast lookup table from a sorted list of [position, color] pairs"""
        # Create hash to check for changes
        gradient_hash = hash(tuple(tuple(pair) for pair in gradient))
        if gradient_hash == self._gradient_hash and self._colormap_cache is not None:
            return self._colormap_cache
        
        # Extract positions and colors directly
        positions = np.array([pos for pos, _ in gradient])
        colors = np.array([self._hex_to_rgb(color) for _, color in gradient])
        
        def fast_colormap(x):
            """Vectorized color interpolation"""
            x = np.asarray(x)
            x_clipped = np.clip(x, 0, 1) * 100
            
            # Find interpolation indices
            indices = np.searchsorted(positions, x_clipped, side='right') - 1
            indices = np.clip(indices, 0, len(positions) - 2)
            
            # Linear interpolation
            t = (x_clipped - positions[indices]) / (positions[indices + 1] - positions[indices])
            t = t[..., np.newaxis]  # Add dimension for color channels
            
            result = colors[indices] * (1 - t) + colors[indices + 1] * t
            return result
        
        self._colormap_cache = fast_colormap
        self._gradient_hash = gradient_hash
        return fast_colormap

    @staticmethod
    def _hex_to_rgb(hex_color):
        """Convert hex color to RGB array (0-1 range)"""
        hex_color = hex_color.lstrip('#')
        return np.array([int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)])

    @staticmethod
    def _rgb_to_hsv(rgb):
        """Convert RGB (0-1 range) to HSV"""
        r, g, b = rgb
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        delta = max_c - min_c
        
        # Hue calculation
        if delta == 0:
            h = 0
        elif max_c == r:
            h = 60 * (((g - b) / delta) % 6)
        elif max_c == g:
            h = 60 * (((b - r) / delta) + 2)
        else:
            h = 60 * (((r - g) / delta) + 4)
        
        # Saturation calculation
        s = 0 if max_c == 0 else delta / max_c
        
        # Value
        v = max_c
        
        return np.array([h, s, v])

    @staticmethod
    def _hsv_to_rgb(hsv):
        """Convert HSV to RGB (0-1 range)"""
        h, s, v = hsv
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if h < 60:
            r, g, b = c, x, 0
        elif h < 120:
            r, g, b = x, c, 0
        elif h < 180:
            r, g, b = 0, c, x
        elif h < 240:
            r, g, b = 0, x, c
        elif h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return np.array([r + m, g + m, b + m])

    @staticmethod
    def _hex_to_hsv(hex_color):
        """Convert hex color to HSV"""
        rgb = e_color_manager._hex_to_rgb(hex_color)
        return e_color_manager._rgb_to_hsv(rgb)

    @staticmethod
    def _hsv_to_hex(hsv):
        """Convert HSV to hex color"""
        rgb = e_color_manager._hsv_to_rgb(hsv)
        return '#' + ''.join([f'{int(c * 255):02x}' for c in rgb])
    
    def _apply_sound_to_light(self, current_volume):
        """Apply sound-to-light modulation based on selected options."""
        # Region Width: 5% min to 100% max (maps volume 0-1 to width)
        if 'regionWidth' in self.sound_to_light_options:
            min_width = 50
            max_width = 100
            self.section_width = (min_width + current_volume * (max_width - min_width)) * 0.005

        # Region Start: Shifts from base start to base start + 50%
        if 'regionStart' in self.sound_to_light_options:
            shift_amount = current_volume * 50  # 0 to 50% shift
            self.section_start = (self._base_section_start + shift_amount) % 100 * self._inv_100

        # Speed: Modulates from 0.5x to 2x base speed
        if 'speed' in self.sound_to_light_options:
            speed_multiplier = 0.5 + current_volume * 1.5  # 0.5x to 2x
            self.speed = self._base_speed * speed_multiplier

        if any(opt in self.sound_to_light_options for opt in ['startHue', 'endHue', 'startSat', 'endSat', 'startVal', 'endVal']):
            modulated_gradient = []
            
            for i, (position, color) in enumerate(self._base_gradient):
                hsv = self._hex_to_hsv(color)
                
                # Modulate first color (gradient start)
                if i == 0:
                    if 'startHue' in self.sound_to_light_options:
                        hue_shift = (current_volume - 0.5) * 90  # -45 to +45
                        hsv[0] = (hsv[0] + hue_shift) % 360

                    if 'startSat' in self.sound_to_light_options:
                        hsv[1] = 1 - current_volume
                    
                    if 'startVal' in self.sound_to_light_options:
                        hsv[2] = current_volume
                
                # Modulate last color (gradient end)
                elif i == len(self._base_gradient) - 1:
                    if 'endHue' in self.sound_to_light_options:
                        hue_shift = (current_volume - 0.5) * 90  # -45 to +45
                        hsv[0] = (hsv[0] + hue_shift) % 360

                    if 'endSat' in self.sound_to_light_options:
                        hsv[1] = 1 - current_volume

                    if 'endVal' in self.sound_to_light_options:
                        hsv[2] = current_volume
                
                modulated_gradient.append([position, self._hsv_to_hex(hsv)])
            
            # Update gradient and recreate colormap
            self.gradient = modulated_gradient
            self._colormap_cache = self._create_fast_colormap(self.gradient)


    def _calculate_gradient_positions(self, base_positions, speed_multiplier=1.0):
        """Shared gradient position calculation"""
        section_start_norm = self.section_start
        section_width_norm = self.section_width
        animation_offset = (self.counter * speed_multiplier * self.speed) % 1.0
        
        section_positions = base_positions * section_width_norm
        final_positions = (section_start_norm + section_positions + animation_offset) % 1.0

        # mirror gradient for smooth transition
        final_positions = np.where(final_positions <= 0.5, final_positions * 2.0, 2.0 * (1.0 - final_positions))

        return final_positions

    def apply_linear_gradient_vectorized(self, world, colormap):
        """Vectorized linear gradient application with rotation support"""
        # Calculate rotation angles based on rotation speeds
        angle_y = self.rotation_counter * self.rotate_speed_y * 2 * np.pi  # Full rotation = 2π
        angle_z = self.rotation_counter * self.rotate_speed_z * 2 * np.pi
        
        # Add sound-to-light rotation (volume 0.5 = no rotation, 0 = -90°, 1 = +90°)
        if 'rotateY' in self.sound_to_light_options:
            sound_angle_y = (self.current_volume - 0.5) * np.pi * 0.5  # -45° to +45°
            angle_y += sound_angle_y
        
        if 'rotateZ' in self.sound_to_light_options:
            sound_angle_z = (self.current_volume - 0.5) * np.pi * 0.5  # -45° to +45°
            angle_z += sound_angle_z
    
        # Get rotated coordinates or use simple X coords if no rotation
        if angle_y != 0 or angle_z != 0:
            base_positions = self._rotate_coordinates(angle_y, angle_z)
        else:
            # No rotation: use simple 1D approach (much faster)
            mirrored_positions = self._calculate_gradient_positions(self._x_coords, speed_multiplier=1.0)
            colors = colormap(mirrored_positions)  # Shape: [10, 3]
            colors_reshaped = colors.T[:, :, np.newaxis, np.newaxis]
            world[:3] *= colors_reshaped
            return world
        
        # Apply gradient calculation to rotated coordinates
        mirrored_positions = self._calculate_gradient_positions(base_positions, speed_multiplier=1.0)
        colors = colormap(mirrored_positions)  # Shape: [10, 10, 10, 3]
        
        # Apply colors (vectorized)
        world[:3] *= colors.transpose(3, 0, 1, 2)
        
        return world

    def apply_radial_gradient_vectorized(self, world, colormap):
        """Vectorized radial gradient application"""
        base_positions = self._distance_cache
        mirrored_positions = self._calculate_gradient_positions(base_positions, speed_multiplier=6.0)
        colors = colormap(mirrored_positions)
        
        # Apply colors (vectorized)
        world[:3] *= colors.transpose(3, 0, 1, 2)
        
        return world

    def __call__(self, world, color_manager_data: dict = None):
        """Optimized main function"""
        # Ensure pre-computed data is available
        if self._x_coords is None:
            self._precompute_coordinates()
        
        # Ensure cached colormap is available
        if self._colormap_cache is None:
            self._colormap_cache = self._create_fast_colormap(self.gradient)

        # Update parameters
        if color_manager_data:
            self.gradient = color_manager_data['gradient']
            self._base_gradient = color_manager_data['gradient']  # Store base gradient
            self.gradient_type = color_manager_data['gradientType']
            self.speed = color_manager_data['speed'] * self._inv_100
            self._base_speed = self.speed
            self.section_start = color_manager_data['sectionStart'] * self._inv_100
            self._base_section_start = color_manager_data['sectionStart']
            self.section_width = color_manager_data['sectionWidth'] * 0.005 # / 100 / 2
            self._base_section_width = color_manager_data['sectionWidth']
            self.rotate_speed_y = color_manager_data['rotateSpeedY'] * self._inv_100
            self._base_rotate_speed_y = color_manager_data['rotateSpeedY']
            self.rotate_speed_z = color_manager_data['rotateSpeedZ'] * self._inv_100
            self._base_rotate_speed_z = color_manager_data['rotateSpeedZ']
            self.sound_to_light_options = color_manager_data.get('soundToLightOptions', [])

            # Update colormap cache
            self._colormap_cache = self._create_fast_colormap(self.gradient)
        
        # Apply Sound to light
        if self.sound_to_light_options:
            self.current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
            self.current_volume = np.clip(self.current_volume, 0.0, 1.0)
            self._apply_sound_to_light(self.current_volume)

        # Apply gradient (vectorized)
        if self.gradient_type == 'radial':
            world = self.apply_radial_gradient_vectorized(world, self._colormap_cache)
        else:  # linear
            world = self.apply_linear_gradient_vectorized(world, self._colormap_cache)
        
        # Update counter
        self.counter += 1 * 0.01
        self.rotation_counter += 1 * 0.01
        
        return np.clip(world, 0, 1)