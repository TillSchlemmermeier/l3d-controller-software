import numpy as np
from channel import class_channel
from world2vox_fortran import world2vox_f as world2vox
import requests
import serial
import time
import multiprocessing as mp
# load shots
from oneshots.s_sides import *
from oneshots.s_blank import *
from oneshots.s_fade import *
from oneshots.s_dark import *
from oneshots.s_growing_sphere import *
from oneshots.s_roll import *
from oneshots.s_strobo import s_strobo
from oneshots.s_cubes import s_cubes
from oneshots.s_dark_sphere import s_dark_sphere
from oneshots.s_threesixty import s_threesixty
from oneshots.s_trigger import s_trigger

from db_manager import DatabaseManager

db = DatabaseManager()
effects = [eff['name'] for eff in db.get_active_elements('effect')]
for effect in effects:
    exec(f'from effects.{effect} import *')

class rendering_engine:
    """
    L3D Cube 4.0

    class for the rendering engine
    """
    def __init__(self):
        """
        Initialises the rendering engine

        Keywords:
        log : enables logging on the debug label
              if false, the rendering engine is logging,
              but only errors/warnings
        """
        # initialise variables
        # self.framecounter = 1
        self.logging = False
        self.connected = False     # Arduino connection status
        self.arduino_message_shown = False

        self.header = [int(66), int(69), int(69), int(70)] # BEEF in ASCII

        # initialize global effects
        self.global_effects = []

        # Initialize timing variables
        self.start_time = time.time()
        self.frame_count = 0

        # one shots
        self.shot_state = 0
        self.shot = s_blank()
        self.shot_list = []
        self.shot_list.append(s_blank)
        self.shot_list.append(s_sides)
        self.shot_list.append(s_fade)
        self.shot_list.append(s_dark)
        self.shot_list.append(s_growing_sphere)
        self.shot_list.append(s_roll)
        self.shot_list.append(s_strobo)
        self.shot_list.append(s_cubes)
        self.shot_list.append(s_dark_sphere)
        self.shot_list.append(s_threesixty)
        self.shot_list.append(s_trigger)

        # try to establish connection to arduino
        try:
            self.arduino = serial.Serial('/dev/ttyACM0', 230400)
            print('Connection to Arduino established')
            print(self.arduino)
            self.connected = True
        except IOError:
            try:
                self.arduino = serial.Serial('/dev/ttyACM1', 230400)
                print('Connection to Arduino established')
                print(self.arduino)
                self.connected = True
            except IOError:
                print('No Connection to Arduino established')

        # setup empty world
        self.cubeworld = np.zeros([3, 10, 10, 10])
        self.channelworld = np.zeros([8, 3, 10, 10, 10])

        # initialise channels
        self.channels = []
        for i in range(1,9):
            self.channels.append(class_channel(i))

        # initialise shared memory
        self.shared_cube_memory = mp.shared_memory.SharedMemory(name="cube_data")
        self.shared_cube_array = np.ndarray((9, 1000, 3), dtype=np.float32, buffer=self.shared_cube_memory.buf)    


    def run(self, state):
        """generates a frame and sends the package when cube is turned on"""
        # check wether 'running' flag is set
        # self.generate_frame(state.data.copy())
        self.generate_frame(state)
        with state.lock:
            state.apply_update() # Ensure we have latest state
            should_send = state['IO']
        if should_send:
            self.send_frame()

        # self.framecounter += 1

        # Prepare combined cube data
        cube_colors = np.zeros([3, 1000])
        cube_colors[0, :] = self.cubeworld[0, :, :, :].flatten()
        cube_colors[1, :] = self.cubeworld[1, :, :, :].flatten()
        cube_colors[2, :] = self.cubeworld[2, :, :, :].flatten()

        # Prepare channel data
        channel_colors = np.zeros([8, 3, 1000])  # 8 channels, 3 color components (RGB), 1000 LEDs
        for i in range(8):
            channel_colors[i, 0, :] = self.channelworld[i, 0, :, :, :].flatten()  # R
            channel_colors[i, 1, :] = self.channelworld[i, 1, :, :, :].flatten()  # G
            channel_colors[i, 2, :] = self.channelworld[i, 2, :, :, :].flatten()  # B

        # Increment frame count
        self.frame_count += 1

        # Calculate elapsed time
        elapsed_time = time.time() - self.start_time

        # Print the frequency every 10 seconds
        if elapsed_time >= 10.0:
            print(f"Run method executed {self.frame_count} times in the last 10 seconds")
            self.frame_count = 0
            self.start_time = time.time()

        # Reshape cube_colors and channel_colors to have consistent dimensions
        cube_colors_reshaped = cube_colors.T.reshape(1, 1000, 3)  # Shape: (1, 1000, 3)
        channel_colors_reshaped = channel_colors.transpose(0, 2, 1)  # Shape: (8, 1000, 3)
        # Concatenate along first axis
        all_colors = np.concatenate([cube_colors_reshaped, channel_colors_reshaped], axis=0)  # Shape: (9, 1000, 3)
        # save to shared memory
        np.copyto(self.shared_cube_array, all_colors)

        # reset cubeworld
        self.cubeworld = np.zeros([3, 10, 10, 10])


    def send_frame(self):
        """
        Function to convert world to voxel format,
        and send it through serial interface to the
        Arduino
        """

        try:
            package = bytearray(self.header + self.get_cubedata())
        except:
            print(self.get_cubedata())

        if self.connected:
            self.arduino.write(package)
        elif not self.arduino_message_shown:
            print('ARDUINO CONNECTION WAS NOT DETECTED, CAN NOT SEND FRAMES')
            self.arduino_message_shown = True


    def generate_frame(self, state):
        """
        Calculates a new frame according to the
        entries in the global parameter variable

        writes the result into self.cubeworld
        """

        # Create copy of state to prevent UltraDict AssertionError
        with state.lock:
            state.apply_update()  # Ensure we have latest state
            snapshot = {
                'numberOfChannels': state['numberOfChannels'],
                'IO': state['IO'],
                'brightness': state['brightness'],
                'oneshot': state['oneshot'],
                'crossfade_active': state['crossfade_active']
            }
            
            # Copy individual channel states
            for i in range(state['numberOfChannels']):
                if i in state:
                    snapshot[i] = dict(state[i])
            
            # Copy global effects
            if 9 in state:
                snapshot[9] = dict(state[9])


        # loop through channels
        for i in range(snapshot['numberOfChannels']):
            channel = self.channels[i]
            this_channel = snapshot[i]
            # check if channel needs to be updated
            if this_channel['update']:
                updated_state = channel.update_channel(this_channel)
                updated_state['update'] = False
                with state.lock:
                    state[i] = updated_state
                    if snapshot['crossfade_active']:
                        state['crossfade_active'] = False
                        requests.get("http://localhost:8000/api/update_key/crossfade_active")

            # check whether channel is active
            new_world, updated_channel = channel.render_frame(this_channel)

            # Only update state if changes occurred
            if updated_channel is not None:
                with state.lock:
                    state[i] = updated_channel

            # apply channel fade
            self.channelworld[i, :, :, :] = new_world + this_channel['fade']*\
                                             self.channelworld[i, :, :, :]

        # copy channels together
        for i in range(snapshot['numberOfChannels']):
            if snapshot[i]['IO']:
                brightness = np.clip(snapshot[i]['brightness'], 0, 1)
                self.cubeworld += brightness * self.channelworld[i, :, :, :]

        # check if global effects need to be updated
        if snapshot[9]['update']:
            with state.lock:
                state[9] = self.update_global_effects(snapshot[9])

        # apply global effect 
        for i in range(snapshot[9]['numberOfEffects']):
            # Update effect state values if needed
            if snapshot[9][i]['update']:
                global_effects = snapshot[9]
                effect_state = self.global_effects[i].return_state()
                for k in range(len(effect_state)):
                    global_effects[i]['params'][4*k:4*k+3] = effect_state[k][:3]
                global_effects[i]['update'] = False
                with state.lock:
                    state[9] = global_effects
            self.cubeworld = self.global_effects[i](self.cubeworld, snapshot[9][i]['params'][3::4])

        # detect whether a oneshot is fired
        if snapshot['oneshot'] > 0:
            print('oneshot fired')
            self.shot_state = snapshot['oneshot']
            self.shot = self.shot_list[int(self.shot_state)]()
            with state.lock:
                state['oneshot'] = 0
            requests.get("http://localhost:8000/api/update_key/oneshot")

        if self.shot_state > 0:
            self.cubeworld, counter = self.shot(self.cubeworld)
            if counter <= 0:
                self.shot_state = 0
                self.shot = s_blank()

        # # Apply global fade
        # self.cubeworld *= state['fade']

        # adjust global brightness
        self.cubeworld *= snapshot['brightness']


    def update_global_effects(self, globalEffects):
        numEffects = globalEffects['numberOfEffects']
        # if global effects were removed, remove them from the list
        if numEffects < len(self.global_effects):
            self.global_effects = self.global_effects[:numEffects]

        # check if global effects need to be updated and if so, loop over them
        for i in range(numEffects):
            this_effect = globalEffects[i]
            if this_effect['update']:
                # if the effect was added, add a new instance to the list
                if i >= len(self.global_effects):
                    exec('self.global_effects.append(' + this_effect['name'] + '())')
                # otherwise check if effect changed and if so, replace old effect with instance of the new one
                elif this_effect['name'] != self.global_effects[i].__class__.__name__:
                    exec('self.global_effects[i] = ' + this_effect['name'] + '()')

        globalEffects['update'] = False
        return globalEffects
    

    def get_cubedata(self):
        """get vox format from the internal stored world"""
        list1 = world2vox(np.nan_to_num(np.clip(self.cubeworld[0, :, :, :], 0, 1)))
        list2 = world2vox(np.nan_to_num(np.clip(self.cubeworld[1, :, :, :], 0, 1)))
        list3 = world2vox(np.nan_to_num(np.clip(self.cubeworld[2, :, :, :], 0, 1)))
        # stack this lists for each color, so that we have RGB ordering for
        # each LED
        liste = list(np.stack((list1, list2, list3)).flatten('F'))
        return liste