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
        self.beatstep = 0

    def return_values(self):
        if self.channel == 4:
            return [b'Letters', b'char', b'beatstep', b'', b'channel']
        else:
            return [b'Letters', b'char', b'', b'', b'channel']


    def return_gui_values(self):
        if 4 > self.channel >= 0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = "Trigger"
        else:
            channel = 'noS2L'


        if self.channel == 4:
            return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(self.char, str(round(self.beatstep,2)), '', channel),'utf-8')


        else:
            return       bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(self.char, '', '', channel),'utf-8')


    def __call__(self, args):
        # parsing input
        if self.channel != 4:
            self.char = chr(int(args[0]*(122-48))+48)
        self.beatstep = int(args[1]*8)
        self.channel = int(args[3]*5)-1

        # create empty world
        world = np.zeros([3, 10, 10, 10])

        self.size = 12
        # self.char = 'X'
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf", self.size)
        img = Image.new(mode = 'L', size = (10, 10), color = (0))


        # check if S2L is activated
        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                self.size = np.clip(current_volume * 30, 2, 30)

        # check for trigger
        elif self.channel == 4:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue+self.beatstep:
                self.lastvalue = current_volume
                if self.counter < 10:
                    self.char = chr(48+self.counter)
                    self.counter += 1
                else:
                    self.counter = 0




        d = ImageDraw.Draw(img)
        w, h = self.font.getsize(self.char)
        # print(w,h,(10-w)/2,(10-h)/2)
        d.text(((10-w)/2,(10-h)/2 -2), self.char,  font = self.font, fill=(255))
        self.frame = np.array(img)[:, ::-1]/255.0

        if np.shape(self.frame)[0] == 10:
            pass
        elif np.shape(self.frame)[0] < 10:
            add = 10 - np.shape(self.frame)[0]
            temp = np.zeros([10, 10])
            temp = self.frame # [ add:-add,  add: -add]
            # temp[int(add/2) : -int(add/2), int(add/2) : -int(add/2)] = self.frame
            self.frame = temp
        else:
            cut = np.shape(self.frame)[0] - 10
            self.frame = self.frame[int(cut/2) : -int(cut/2), int(cut/2) : -int(cut/2)]




        # copy world from storate to world
        world[0,:,4,:] = self.frame
        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        # return world
        return np.clip(world,0,1)
