import numpy as np
from PIL import Image, ImageDraw, ImageFont

class g_letters():
    def __init__(self):
        self.char = 'a'
        self.size = 1
        self.frame = []
        font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf", 13)

    def control(self, letter, blub1, blub2):
        self.char = chr(int(letter*127))

    def label(self):
        return ['char',self.char,'empty','empty','empty','empty', 'empty']

    def generate(self, step, dumpworld):
        # create empty world
        world = np.zeros([3, 10, 10, 10

        img = Image.new(mode = 'L', size = (self.size, self.size), color = (0))
        d = ImageDraw.Draw(img)
        d.text((2,-2), self.char,  font = font, fill=(255))
        self.frame = np.array(img)[:, ::-1]/255.0

        if self.size < 30:
            self.size += 1
        else:
            self.size = 1


        # copy world from storate to world
        world[0,:,4,:] = self.frame
        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]


        # return world
        return np.clip(world,0,1)
