import numpy as np
import struct
from PIL import Image, ImageDraw, ImageFont
from multiprocessing import shared_memory

class g_letters():
    '''
    Generator: Letters
    Shows letters in the middle of the Cube

    Parameters:
    - char to show
    - s2l channel

    if trigger is chosen:
    - beatstep = change char every x trigger
    - triggermode:
        - size: char "explodes"
        - countdown from 9 to 0, restart
        - countup from 0 to 9, restart
        - countdown from 9 to 0, "explode" every char
        - countup from 0 to 9, "explode" every char
    '''

    def __init__(self):
        self.char = 'a'
        self.runtime_char = 'a'
        self.size = 12
        self.frame = []
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf", 13)
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0
        self.counter = 0
        self.beatstep = 0
        self.step = 0
        self.triggermode = 0

    def return_state(self):
        return [
            [
                'char',
                'size',
                '-' if self.channel == 'Trigger' else self.char
            ],
            [
                'trigger step',
                'beatstep',
                round(self.beatstep,2) if self.channel == 'Trigger' else '-'
            ],
            [
                'trigger mode',
                'triggermode',
                self.triggermode if self.channel == 'Trigger' else '-'
            ],
            ['channel', 'channel', self.channel],
        ]

    def __call__(self, args):
        # === PARAMETERS START ===
        self.char = chr(int(args[0]*(122-48))+48)
        self.beatstep = int(args[1]*8)
        self.triggermode = ['size', 'countdown', 'countup', 'down+size', 'up+size'][int(args[2]*4)]
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][round(args[3]*5)]
        # === PARAMETERS END ===

        # create empty world
        world = np.zeros([3, 10, 10, 10])

        if self.channel == 'noS2L':
            self.size = 12

        if self.channel != 'Trigger':
            self.runtime_char = self.char

        self.font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf", self.size)
        img = Image.new(mode = 'L', size = (10, 10), color = (0))


        # check if S2L is activated
        if isinstance(self.channel, int):
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
            if current_volume > 0:
                self.size = int(np.clip(current_volume * 30, 2, 30))

        # check for trigger
        elif self.channel == 'Trigger':
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            if current_volume > self.lastvalue+self.beatstep:
                self.lastvalue = current_volume
                self.step = 0

                # countdown or countdown with size mode
                if self.triggermode == 'countdown' or self.triggermode == 'down+size':
                    if self.counter > 8:
                        self.counter = 0
                    else:
                        self.counter += 1

                    self.runtime_char = chr(57-self.counter)

                # count up or count up with size mode
                elif self.triggermode == 'countup' or self.triggermode == 'up+size':
                    if self.counter < 10:
                        self.runtime_char = chr(48+self.counter)
                        self.counter += 1
                    else:
                        self.counter = 0

            # size mode or countdown/countup with size
            if self.triggermode in ['size', 'down+size', 'up+size']:
                if self.step == 0:
                    self.size = 0

                if self.step < 20:
                    self.size += self.step
                    self.step += 1
                else:
                    self.size = 0

            else:
                self.size = 12


        d = ImageDraw.Draw(img)
        w, h = self.font.getsize(self.runtime_char)
        # print(w,h,(10-w)/2,(10-h)/2)
        d.text(((10-w)/2,(10-h)/2 -2), self.runtime_char,  font = self.font, fill=(255))
        self.frame = np.array(img)[:, ::-1]/255.0

        if np.shape(self.frame)[0] == 10:
            pass
        elif np.shape(self.frame)[0] < 10:
            add = 10 - np.shape(self.frame)[0]
            temp = np.zeros([10, 10])
            temp = self.frame
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
