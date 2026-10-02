from scipy.ndimage.interpolation import rotate

class s_threesixty:

    def __init__(self):
        self.counter = 36

    def __call__(self, world):
        for i in range(3):
            # rotate
            world[i, :, :, :] = rotate(world[i, :, :, :], self.counter*10,
                              axes = (1,2), order = 1,
    	                      mode = 'nearest', reshape = False)

        if self.counter >= 0:
            self.counter -= 1


        return world, self.counter
