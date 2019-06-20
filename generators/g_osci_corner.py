
import numpy as np

class g_osci_corner():
    '''
    Generator: corner
    '''

    def __init__(self):
        self.speed = 10

    def control(self, speed, blub1, blub2):
        self.speed = round(1+(speed*50))

    def label(self):
        return ['frame period',round(self.speed,2),'empty','empty','empty','empty','empty']

    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

        # switch on corners
        world[:,0,0,0] = np.sin(step*np.pi*2/self.speed + (np.pi*0)/8.0)
        world[:,0,0,9] = np.sin(step*np.pi*2/self.speed + (np.pi*1)/8.0)
        world[:,0,9,0] = np.sin(step*np.pi*2/self.speed + (np.pi*2)/8.0)
        world[:,9,0,0] = np.sin(step*np.pi*2/self.speed + (np.pi*3)/8.0)
        world[:,0,9,9] = np.sin(step*np.pi*2/self.speed + (np.pi*4)/8.0)
        world[:,9,0,9] = np.sin(step*np.pi*2/self.speed + (np.pi*5)/8.0)
        world[:,9,9,0] = np.sin(step*np.pi*2/self.speed + (np.pi*6)/8.0)
        world[:,9,9,9] = np.sin(step*np.pi*2/self.speed + (np.pi*7)/8.0)

        return np.clip(world, 0, 1)
