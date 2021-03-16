# modules
import numpy as np
from scipy.signal import sawtooth
from multiprocessing import shared_memory

class g_planes():
    '''
    Generator: panes
    a plane moving up and down the cube

    Parameters:
    speed
    direction (x, y or z)
    type (cosinus, up or down)
    Sound2Light trigger On / Off
    '''
    def __init__(self):
        self.speed = 10
        self.dir = 1
        self.type = 0
        self.step = 0
        self.position = 0
        # s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.trigger = False
        self.lastvalue = 0
        self.nextposition = 0
        self.switch = False
        self.stop = False

    #Strings for GUI
    def return_values(self):
        return [b'Planes', b'Speed', b'Direction', b'Type', b'Trigger']

    def return_gui_values(self):
        if self.dir == 0:
            dir = 'X'
        elif self.dir == 1:
            dir ='Y'
        else:
            dir = 'Z'

        if self.type < 0.33:
            type = 'cos'
        elif self.type >= 0.33 and self.type < 0.66:
            type = 'up'
        else:
            type = 'down'

        if self.trigger:
            trigger = 'On'
        else:
            trigger = 'Off'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.speed,2)), dir, type, trigger),'utf-8')


    def __call__(self, args):
        # parsing input
        self.speed = int(args[0]*8)
        self.dir = int(round(args[1]*3))
        self.type = args[2]

        if args[3] < 0.5:
            self.trigger = False
        else:
            self.trigger = True

        #def generate(self, step, dumpworld):
        world = np.zeros([3, 10, 10, 10])

        #check for trigger
        if self.trigger:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.step = 0
                self.switch = False
                self.stop = False
                if self.type < 0.66:
                    self.nextposition = 0
                else:
                    self.nextposition = 9

            if not self.stop:
                self.position = self.nextposition
                if self.type < 0.33:
                    nextposition = 9-int(round((np.cos(0.1*(self.step+1)*self.speed)+1)*4.5))
                    if nextposition < self.position:
                        self.switch = True

                    if self.switch:
                        if nextposition > self.position:
                            self.stop = True

                elif self.type >= 0.33 and self.type < 0.66:
                    nextposition = int(round((sawtooth(0.1*(self.step+1)*self.speed)+1)*4.5))
                    if nextposition < self.position:
                        self.stop = True

                else:
                    nextposition = int(round((sawtooth(0.1*(self.step+1)*self.speed, width=0)+1)*4.5))
                    if nextposition > self.position:
                        self.stop = True

                if not self.stop:
                    self.step += 1
                    self.nextposition = nextposition


        else:
            if self.type < 0.33:
                self.position = 9-int(round((np.cos(0.1*self.step*self.speed)+1)*4.5))
            elif self.type >= 0.33 and self.type < 0.66:
                self.position = int(round((sawtooth(0.1*self.step*self.speed)+1)*4.5))
            else:
                self.position = int(round((sawtooth(0.1*self.step*self.speed, width=0)+1)*4.5))

            self.step += 1


        if self.dir == 0:
            world[:, self.position,:,:] = 1.0
        elif self.dir == 1:
            world[:, :, self.position,:] = 1.0
        else:
            world[:, :,:,self.position] = 1.0

        '''
        # delete if idle?
        if self.trigger:
            if self.stop:
                world[:, :, :, :] = 0.0
        '''

        return np.clip(world, 0, 1)
