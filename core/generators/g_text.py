# modules
import numpy as np
from scipy.signal import sawtooth
from PIL import Image, ImageDraw, ImageFont


class g_text():
    '''
    Generator: text

    '''
    def __init__(self):

        self.strings = []
        self.strings.append('F115BLEIBT')
        self.strings.append('FLORABLEIBT')
        self.strings.append('Subspace')
        self.strings.append('HAPPY BIRTHDAY TIM! ')
        self.strings.append('ANNIKA ')
        self.strings.append('NINA ')
        self.strings.append('ACAB ')
        self.strings_img = []
        for string in self.strings:
            frames = []
            font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf", 13)
            chars = self.split_string(string)

            for c in chars:
                img = Image.new(mode = 'L', size = (10, 10), color = (0))
                d = ImageDraw.Draw(img)
                d.text((2,-2), c,  font = font, fill=(255))
                frames.append(np.array(img)[:, ::-1]/255.0)

            self.strings_img.append(frames)


        self.current_text = 0

        self.counter = 0
        self.framecounter = 1
        self.max = len(self.strings_img[self.current_text])
        self.wait = 5
        self.mode = 'static'

    def split_string(self, word):
        return [char for char in word]

    def return_state(self):
        return [
            ['wait', 'wait', self.wait],
            ['mode', 'mode', self.mode],
            ['string', 'current_text', self.strings[self.current_text]],
        ]
    
    def __call__(self, args):
        # === PARAMETERS START ===
        self.wait = int(args[0]*10)+1
        self.mode = ['static', 'moving'][round(args[1])]
        self.current_text = int((args[2]-0.01)*len(self.strings))
        # === PARAMETERS END ===


        self.max = len(self.strings_img[self.current_text])

        # create empty world
        world = np.zeros([3, 10, 10, 10])

        # choose correct world according to step
        if self.counter >= self.max:
            self.counter = 0

        if self.mode == 'static':

            # copy world from storate to world
            world[0,:,-1,:] = self.strings_img[self.current_text][self.counter]

            # increase counter
            if self.framecounter % self.wait == 0:
                self.counter += 1

        elif self.mode == 'moving':
            world[0,:,-self.framecounter %10,:] = self.strings_img[self.current_text][self.counter]
            if self.framecounter % 10 == 0:
                self.counter += 1

        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        self.framecounter += 1
        return world
