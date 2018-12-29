
import numpy as np

class rendering_engine():
    '''
    L3D Cube 3.0
    
    class for the rendering engine
    
    assuming a global variable called
    'global_parameter':
    - numpy array with size of 255
    - entries ordered as described in
      readme
      
    '''
    def __init__(self):
        # open connections, if possible
        # otherwise write in textfile or so
        
        # initialise variables
        self.framecounter = 0
        
    def run(self):
        # check wether 'running' flag is set
        if global_parameter[0] == 1:
            # increase framecounter
            self.framecounter += 1
            # some test to emulate output to arduino
            print(self.framecounter)
            
            
            
            