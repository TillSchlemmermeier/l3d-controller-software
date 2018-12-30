
import numpy as np
import logging, serial

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
    def __init__(self, log = False):
        
        # initialise variables
        self.framecounter = 0
        self.logging = log
        self.debug = False
        
        self.header =   [int(66),
                         int(69),
                         int(69),
                         int(70),
                         int(1),	# Speed
                         int(200),	# Brightness
                         int(116),	# hPal
                         int(0),	# hPalMode
                         int(1),	# hRGBMode
                         ]
                
        # take care of logging
        if self.logging:
            logging.basicConfig(filename='log_rendering_enginge.log',
                                level=logging.DEBUG)
        else:
            logging.basicConfig(filename='log_rendering_enginge.log',
                                level=logging.WARNING)
        
        logging.info('Variables initialised')
        

        # try to establish connection to arduino
        try:
            self.arduino = serial.Serial('/dev/ttyACM0', 230400)
            logging.info('Connection to Arduino established')
            logging.info(self.arduino)
        except IOError:
            self.arduino = serial.Serial('/dev/ttyACM1', 230400)
            logging.info('Connection to Arduino established')
            logging.info(self.arduino)
	except:
	    self.debug = True
	    logging.warning('No Connection to Arduino established, entering DEBUG mode')

        
    def run(self):
        # check wether 'running' flag is set
        if global_parameter[0] == 1:
            self.generate_frame()
            self.send_frame()
            # increase framecounter
            self.framecounter += 1
            # some test to emulate output to arduino
            print(self.framecounter)
            
            
            
    def send_frame(self):
        '''
        Function to convert world to voxel format,
        and send it through serial interface to the
        Arduino
        '''
        if not self.debug:
            # assemble list
            package = self.header + self.get_cubedata()
            # send package 
            self.arduino.write(bytearray(package))
        else:
            logging.info(self.get_cubedata())
            

    def generate_frame(self):
        '''
        Calculates a new frame according to the
        entries in the global parameter variable
        
        writes the result into self.cubeworld
        '''
        pass
        
    def get_cubedata(self):
        '''
        takes data from self.cubeworld and returns
        voxel-style list
        '''
        pass