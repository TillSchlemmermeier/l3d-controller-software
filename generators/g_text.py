import numpy as np
from PIL import Image, ImageDraw, ImageFont

class g_text():
    def __init__(self):

        chars = ['F', '1', '1', '5', 'B', 'L', 'E', 'I', 'B', 'T']

        self.frames = []
        font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf", 13)

        for c in chars:
            img = Image.new(mode = 'L', size = (10, 10), color = (0))
            d = ImageDraw.Draw(img)
            d.text((2,-2), c,  font = font, fill=(255))
            self.frames.append(np.array(img)[:, ::-1]/255.0)

        self.counter = 0
        self.max = len(self.frames)
        self.wait = 5

    def control(self, wait, blub1, blub2):
        self.wait = int(wait*10)+1

    def label(self):
        return ['wait',round(self.wait,2),'empty','empty','empty','empty', 'empty']

    def generate(self, step, dumpworld):
        # create empty world
        world = np.zeros([3, 10, 10, 10])

        # choose correct world according to step
        if self.counter >= self.max:
            self.counter = 0

        # copy world from storate to world
        world[0,:,-1,:] = self.frames[self.counter]
        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        # increase counter
        if step % self.wait == 0:
            self.counter += 1

        # return world
        return np.clip(world,0,1)
