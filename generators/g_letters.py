import numpy as np
from PIL import Image, ImageDraw, ImageFont

class g_letters():
    def __init__(self):
        self.char = 'a'
        self.size = 2
        self.frame = []
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf", 13)

    def return_values(self):
        return [b'Letters', b'char', b'', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(self.char, '', '', ''),'utf-8')


    def __call__(self, args):
        # parsing input
        self.char = chr(int(args[0]*127)+97)

        # create empty world
        world = np.zeros([3, 10, 10, 10])

        self.size = 8
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf", self.size)
        img = Image.new(mode = 'L', size = (self.size, self.size), color = (0))

        d = ImageDraw.Draw(img)
        d.text((0, -2), 'X',  font = self.font, fill=(255))# , anchor = 'rs')
        self.frame = np.array(img)[:, ::-1]/255.0

        if np.shape(self.frame)[0] == 10:
            pass
        elif np.shape(self.frame)[0] < 10:
            add = 10 - np.shape(self.frame)[0]
            temp = np.zeros([10, 10])
            temp[1 : -1, 1 : -1] = self.frame
            # temp[int(add/2) : -int(add/2), int(add/2) : -int(add/2)] = self.frame
            self.frame = temp
        else:
            cut = np.shape(self.frame)[0] - 10
            self.frame = self.frame[int(cut/2) : -int(cut/2), int(cut/2) : -int(cut/2)]

        if self.size < 30:
            self.size += 2
        else:
            self.size = 2

        # copy world from storate to world
        world[0,:,4,:] = self.frame
        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        # return world
        return np.clip(world,0,1)
