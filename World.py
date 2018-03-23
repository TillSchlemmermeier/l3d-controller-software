import numpy as np

class CubeWorld:

    def __init__(self):
        # initialize worlds at startup
        # indices: [color, x, y, z]

        # world for channel A
        world_CHA = np.zeros([3,10,10,10])
        # world for channel B
        world_CHB = np.zer0s([3,10,10,10])
        # world for master
        world_TOT = np.zeros([3,10,10,10])

        framecounter = 0


    def get_cubedata(self):
        # returns string(bytestream?) to
        # send to the arduino

        def world2str():
            # converts world_tot to string
            # ...

        return world2str(self.world_TOT)


    def test_screen(self, clear = True):
        # creates a test_screen to check orientation
        # and proper colours

        # clears world matrices if clear == True
        if clear:
            self.world_CHA[:,:,:,:] = 0
            self.world_CHB[:,:,:,:] = 0
            self.world_TOT[:,:,:,:] = 0

        # draw something in the red channel
        # of channel A
        self.world_CHA[0,:1,0,0] = 1
        self.world_CHA[0,0,:2,0] = 1
        self.world_CHA[0,0,0,:3] = 1

        # draw something in the blue channel
        # of channel B
        self.world_CHA[2,0,0,0] = 1
        self.world_CHA[2,9,0,0] = 1
        self.world_CHA[2,0,9,0] = 1
        self.world_CHA[2,0,0,9] = 1
        self.world_CHA[2,0,9,9] = 1
        self.world_CHA[2,9,0,9] = 1
        self.world_CHA[2,9,9,0] = 1
        self.world_CHA[2,9,9,9] = 1


    def update(self):
        # updates the world matrices according
        # to assigned generators and filters

        # Channel A
        # Generators
        # Effects

        # Channel B
        # Generators
        # Effects

        # Sum Channels
        self.world_TOT = self.world_CHA + self.world_CHB
        # or self.world_TOT += self.world_CHA + self.world_CHB?

        # Global Effects

        self.framcounter += 1
