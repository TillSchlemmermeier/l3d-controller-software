import numpy as np

class e_compressor():
    '''Effect: compressor'''

    def __init__(self):
        self.amount = 1.0
        self.smooth = 0.5
        self.factor = 1.0

    def return_state(self):
        return [
            ['Amount', 'amount', round(self.amount,1)],
            ['Smooth', 'smooth', round(self.smooth,1)],
        ]

    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.amount = args[0]
        self.smooth = args[1]
        # === PARAMETERS END ===

        # get brightness
        brightness = np.sum(np.clip(world, 0, 1))        

        # calculate factor
        self.factor = (1-np.sqrt(np.clip(self.amount*brightness/1000, 0, 1))) *\
                      (1-self.smooth) + self.factor * self.smooth
        
        world *= np.clip(self.factor,0,1E2)

        return np.clip(world, 0, 1)
