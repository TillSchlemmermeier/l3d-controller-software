import numpy as np
from random import choice
from scipy.ndimage.interpolation import rotate

class g_falling():
    def __init__(self):
        # Animation state
        self.step = 0
        self.wait = 1
        self.plane_rotation = 0
        self.rotating = False
        self.rotation_step = 0
        self.rotation_angle = 0
        self.bigworld = np.zeros([21, 21, 10])
        self.bigworld[10, 1:-1, :] = 1.0  
        self.counter = 1

        self.particles = []
        self.reset_particles()
    
    def reset_particles(self):
        self.particles = []
        for y in range(10):
            for z in range(10):
                # [x, y, z, falling, landed]
                self.particles.append([0, y, z, False, False])
    
    def return_state(self):
        return [
            ['wait', 'wait', round(self.wait, 2)],
        ]
    
    def __call__(self, args):
        # === PARAMETERS START ===
        self.wait = int(args[0] * 10) + 1
        # === PARAMETERS END ===
        world = np.zeros([3, 10, 10, 10])

        # Handle rotation transition
        if self.rotating:
            self.rotation_angle += int(4 / self.wait) + 1
            if self.rotation_angle >= 90:
                self.rotation_step += 1
                if self.rotation_step == 2:
                    self.rotating = False
                    self.rotation_step = 0
                    self.reset_particles()
                self.rotation_angle = 0

            if self.rotating:
                # Apply rotation
                newworld = rotate(self.bigworld, self.rotation_angle,
                                axes=(0, 1), order=1,
                                mode='nearest', reshape=False)[1:11, 10:-1, :]
                
                if self.rotation_step == 1:
                    newworld = np.rot90(newworld, k = 3, axes = (0,1))

                world[:, :, :, :] = newworld
            else:  
                for particle in self.particles:
                    x, y, z, _, _ = particle
                    world[:, x, y, z] = 1.0
            
        else:
            # Normal falling animation
            if not self.rotating and self.step % self.wait == 0:
                # Start new particle falling
                non_falling = [p for p in self.particles if not p[3] and not p[4]]
                if non_falling:
                    particle = choice(non_falling)
                    particle[3] = True  # Start falling
                
                # Update falling particles
                all_landed = True
                for particle in self.particles:
                    if particle[3] and not particle[4]:  # If falling
                        if particle[0] < 9:  # If not at bottom
                            new_x = particle[0] + 1
                            # Check if space to the left is empty
                            if not any(p[0] == new_x and 
                                    p[1] == particle[1] and 
                                    p[2] == particle[2] and 
                                    p[4] for p in self.particles):
                                particle[0] = new_x
                            else:
                                particle[4] = True  # Landed
                        else:
                            particle[4] = True  # Landed at left side
                    
                    if not particle[4]:  # If not landed
                        all_landed = False
                
                # If all particles have landed, start rotation
                if all_landed:
                    self.rotating = True
            
            # Draw particles
            for particle in self.particles:
                x, y, z, _, _ = particle
                world[:, x, y, z] = 1.0

        
        self.step += 1
        return np.clip(world, 0, 1)