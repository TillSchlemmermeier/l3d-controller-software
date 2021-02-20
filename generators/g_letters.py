import numpy as np
from PIL import Image, ImageDraw, ImageFont
from multiprocessing import shared_memory

class g_letters():
    def __init__(self):
        self.char = 'a'
        self.size = 2
        self.frame = []
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf", 13)
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0
        self.counter = 0

    def return_values(self):
        return [b'Letters', b'char', b'', b'', b'channel']

    def return_gui_values(self):
        if 4 > self.channel >= 0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = "Trigger"
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(self.char, '', '', channel),'utf-8')


    def __call__(self, args):
        # parsing input
        self.char = chr(int(args[0]*127)+97)
        self.channel = int(args[3]*5)-1

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

        # check if S2L is activated
        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                self.size = np.clip(current_volume * 30, 2, 30)

        #check for trigger
        elif self.channel == 4:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.size = 2

            if self.size < 30:
                self.size += 2

        elif self.size < 30:
            self.size += 2
        else:
            self.size = 2

        # copy world from storate to world
        world[0,:,4,:] = self.frame
        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        # return world
        return np.clip(world,0,1)
