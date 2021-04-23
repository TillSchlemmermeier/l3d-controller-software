# modules
import numpy as np
from scipy.ndimage.interpolation import rotate
from multiprocessing import shared_memory
from random import randint, choice
from itertools import cycle

class g_obliqueplane_new():
    def __init__(self):
        self.speed = 0.1
        self.step = 0
        self.axes = [0, 1]
        self.n_rot = 1
        self.combinations = [[0 , 1], [0 , 2],[1, 2], [1, 0], [2, 0], [2, 1]]
        self.real_speed = 0
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.trigger = False
        self.lastvalue = 0
        self.counter = 0
        self.side1 = 1
        self.side2 = choice([2,4])
        self.mode = 'chain'

        self.connections = {}
        self.connections[1] = [2,4,5,6]
        self.connections[2] = [1,3,5,6]
        self.connections[3] = [2,4,5,6]
        self.connections[4] = [1,3,5,6]
        self.connections[5] = [1,2,3,4]
        self.connections[6] = [1,2,3,4]

        self.circle_iter = cycle([1,2,3,4])

        #create bigworld
        self.bigworld = np.zeros([21, 21, 10])

        #self.bigworld[10, 1:-1, 1:-1] = 1.0
        self.bigworld[10, 1:-1, :] = 1.0
        self.counter = 1

    #Strings for GUI
    def return_values(self):
        return [b'rotate_plane', b'speed', b'modus', b'zspeed', b'Trigger']


    def return_gui_values(self):
        if self.trigger:
            trigger = 'On'
        else:
            trigger = 'Off'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.speed,2)), self.mode,'', trigger),'utf-8')


    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.speed = 20*args[0]
        if args[1] > 0.75:
            self.mode = 'forward'
        elif args[1] > 0.5 and args[1] <= 0.75:
            self.mode = 'chain'
        elif args[1] > 0.25 and args[1] <= 0.5:
            self.mode = 'circle'
        else:
            self.mode = 'random'

        if args[3] > 0.1:
            self.trigger = True
        else:
            self.trigger = False

        # create world
        world = np.zeros([3, 10, 10, 10])



        self.real_speed = self.step*self.speed
        if self.real_speed > 90:
            if self.trigger:
                current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
                if current_volume > self.lastvalue:
                    self.lastvalue = current_volume
                    self.step = 0

                    self.real_speed = self.step*self.speed
                    if self.mode == 'random':
                        #self.axes = choice(self.combinations)
                        #self.n_rot = randint(1,3)
                        self.side1 = randint(1,6)
                        self.side2 = choice(self.connections[self.side1])
                    elif self.mode == 'chain':
                        self.side1 = self.side2
                        self.side2 = choice(self.connections[self.side1])
                    elif self.mode == 'forward':
                        temp = self.side1
                        self.side1 = self.side2
                        while True:
                            self.side2 = choice(self.connections[self.side1])
                            if self.side2 != temp:
                                break
                    elif self.mode == 'circle':
                #        print(self.side1, self.side2)
                        self.side1 = self.counter%4+1
                        self.side2 = (self.counter+1)%4+1 # next(self.circle_iter)
                        #print(self.step, self.side1, self.side2)
                        self.counter += 1

                else:
                    self.step -= 1
                    self.real_speed = 90
            else:
                self.step = 0

                self.real_speed = self.step*self.speed
                if self.mode == 'random':
                    #self.axes = choice(self.combinations)
                    #self.n_rot = randint(1,3)
                    self.side1 = randint(1,6)
                    self.side2 = choice(self.connections[self.side1])
                elif self.mode == 'chain':
                    self.side1 = self.side2
                    self.side2 = choice(self.connections[self.side1])
                elif self.mode == 'forward':
                    temp = self.side1
                    self.side1 = self.side2
                    while True:
                        self.side2 = choice(self.connections[self.side1])
                        if self.side2 != temp:
                            break
                elif self.mode == 'circle':
            #        print(self.side1, self.side2)
                    self.side1 = self.counter%4+1
                    self.side2 = (self.counter+1)%4+1 # next(self.circle_iter)
                    #print(self.step, self.side1, self.side2)
                    self.counter += 1

        self.step += 1

        # rotate
        newworld = rotate(self.bigworld, self.real_speed,
                          axes = (0,1), order = 1,
	                      mode = 'nearest', reshape = False)[1:11, 10:-1, :]


        # insert array
        newworld = self.get_transition(newworld, self.side1, self.side2)

        #print(np.shape(newworld ))

        world[:, :, :, :] = newworld


        return np.clip(world, 0, 1)


    def get_transition(self, newworld, side1, side2):
        #print('from', side1, 'to', side2)
        if side1 == 1 and side2 == 2:
            return newworld
        elif side1 == 1 and side2 == 4:
            return np.rot90(newworld, k = 2, axes = (1,2))
        elif side1 == 1 and side2 == 5:
            return np.rot90(newworld, k = 1, axes = (1,2))
        elif side1 == 1 and side2 == 6:
            return np.rot90(newworld, k = 3, axes = (1,2))

        elif side1 == 2 and side2 == 3:
            return np.rot90(newworld, k = 3, axes = (0,1))
        elif side1 == 2 and side2 == 5:
            temp = np.rot90(newworld, k = 3, axes = (0,1))
            return np.rot90(temp, k = 1, axes = (0,2))
        elif side1 == 2 and side2 == 6:
            temp = np.rot90(newworld, k = 3, axes = (0,1))
            return np.rot90(temp, k = 3, axes = (0,2))
        elif side1 == 2 and side2 == 1:
            temp = np.rot90(newworld, k = 3, axes = (0,1))
            return np.rot90(temp, k = 2, axes = (0,2))

        elif side1 == 3 and side2 == 4:
            return np.rot90(newworld, k = 2, axes = (0,1))
        elif side1 == 3 and side2 == 6:
            temp = np.rot90(newworld, k = 2, axes = (0,1))
            return np.rot90(temp, k = 1, axes = (1,2))
        elif side1 == 3 and side2 == 5:
            temp = np.rot90(newworld, k = 2, axes = (0,1))
            return np.rot90(temp, k = 3, axes = (1,2))
        elif side1 == 3 and side2 == 2:
            temp = np.rot90(newworld, k = 2, axes = (0,1))
            return np.rot90(temp, k = 2, axes = (1,2))

        elif side1 == 4 and side2 == 1:
            return np.rot90(newworld, k = 1, axes = (0,1))
        elif side1 == 4 and side2 == 6:
            temp = np.rot90(newworld, k = 1, axes = (0,1))
            return np.rot90(temp, k = 1, axes = (0,2))
        elif side1 == 4 and side2 == 5:
            temp = np.rot90(newworld, k = 1, axes = (0,1))
            return np.rot90(temp, k = 3, axes = (0,2))
        elif side1 == 4 and side2 == 3:
            temp = np.rot90(newworld, k = 1, axes = (0,1))
            return np.rot90(temp, k = 2, axes = (0,2))

        elif side1 == 5 and side2 == 2:
            return np.rot90(newworld, k = 3, axes = (0,2))
        elif side1 == 5 and side2 == 1:
            temp = np.rot90(newworld, k = 3, axes = (0,2))
            return np.rot90(temp, k = 1, axes = (0,1))
        elif side1 == 5 and side2 == 3:
            temp = np.rot90(newworld, k = 3, axes = (0,2))
            return np.rot90(temp, k = 3, axes = (0,1))
        elif side1 == 5 and side2 == 4:
            temp = np.rot90(newworld, k = 3, axes = (0,2))
            return np.rot90(temp, k = 2, axes = (0,1))

        elif side1 == 6 and side2 == 2:
            return np.rot90(newworld, k = 1, axes = (0,2))
        elif side1 == 6 and side2 == 1:
            temp = np.rot90(newworld, k = 1, axes = (0,2))
            return np.rot90(temp, k = 1, axes = (0,1))
        elif side1 == 6 and side2 == 3:
            temp = np.rot90(newworld, k = 1, axes = (0,2))
            return np.rot90(temp, k = 3, axes = (0,1))
        elif side1 == 6 and side2 == 4:
            temp = np.rot90(newworld, k = 1, axes = (0,2))
            return np.rot90(temp, k = 2, axes = (0,1))
