import numpy as np
from channel import class_channel
from world2vox_fortran import world2vox_f as world2vox
import requests
import serial
import time
import copy
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

from effects.e_color_manager import e_color_manager

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
        """
        # initialise variables
        self.logging = False
        self.connected = False     # Arduino connection status
        self.arduino_message_shown = False

        self.header = [int(66), int(69), int(69), int(70)] # BEEF in ASCII

        # initialize global effects
        self.global_effects = []

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

        self.global_color_effect = e_color_manager()

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

        # wether to send data to arduino
        self.should_send = False

        # setup empty world
        self.cubeworld = np.zeros([3, 10, 10, 10])
        self.channelworld = np.zeros([8, 3, 10, 10, 10])

        # initialise channels
        self.channels = []
        print('Initialising Channels...')
        for i in range(1,9):
            self.channels.append(class_channel(i))
        print('Channels Initialised')

        # initialise shared memory
        self.shared_cube_memory = mp.shared_memory.SharedMemory(name="cube_data")
        self.shared_cube_array = np.ndarray((9, 1000, 3), dtype=np.uint8, buffer=self.shared_cube_memory.buf)
        self.stage_buffer = np.zeros((9, 1000, 3), dtype=np.float64)


    def run(self, state):
        """generates a frame and sends the package when cube is turned on"""

        self.generate_frame(state)

        if self.should_send:
            self.send_frame()

        # Pack combined + per-channel colors into the (9,1000,3) staging buffer.
        # reshape/transpose return views (no copy)
        #   row 0     = combined cube  (cubeworld    (3,10,10,10)   -> (1000,3))
        #   rows 1..8 = the 8 channels (channelworld (8,3,10,10,10) -> (8,1000,3))
        self.stage_buffer[0] = self.cubeworld.reshape(3, 1000).T
        self.stage_buffer[1:9] = self.channelworld.reshape(8, 3, 1000).transpose(0, 2, 1)

        # quantize float [0,1] -> uint8 [0,255]: matches the cube's 8-bit depth
        np.clip(self.stage_buffer, 0.0, 1.0, out=self.stage_buffer)
        self.stage_buffer *= 255.0
        self.shared_cube_array[:] = self.stage_buffer.astype(np.uint8)


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
            print('----------------------------------------------------\n' \
            'NO ARDUINO DETECTED, PLEASE CONNECT AND REBOOT CORE\n' \
                '-----------------------------------------------------\n')
            self.arduino_message_shown = True


    def generate_frame(self, state):
        """
        Calculates a new frame according to the
        entries in the global parameter variable

        writes the result into self.cubeworld
        """

        retry_count = 0
        snapshot = None
        while retry_count < 3:
            try:
                # Create copy of state to prevent UltraDict AssertionError
                with state.lock:
                    state.apply_update()
                    snapshot = copy.deepcopy(state.data)
                    # shallow copy alternative:
                    # snapshot = dict(state)
                    self.should_send = snapshot['IO']
                break

            except AssertionError as e:
                print(f"[CORE] UltraDict buffer corruption (attempt {retry_count + 1}/3)")
                retry_count += 1
                if retry_count >= 3:
                    print(f"[CORE] Giving up after 3 attempts, skipping frame")
                    return
                # Wait for MIDI burst to finish
                time.sleep(0.02 * retry_count)

            except Exception as e:
                import traceback
                print(f"[CORE] Unexpected error (attempt {retry_count + 1}/3): {type(e).__name__}: {e}")
                traceback.print_exc()
                retry_count += 1
                if retry_count >= 3:
                    print(f"[CORE] Fatal error, skipping frame")
                    return
                time.sleep(0.02 * retry_count)

        if snapshot is None:
            print("[CORE] No valid snapshot created, skipping frame")
            return

        pending_update = {}
        clear_color_update = False
        reset_oneshot = False

        # loop through channels
        for i in range(snapshot['numberOfChannels']):
            channel = self.channels[i]
            this_channel = snapshot[i]
            # check if channel needs to be updated
            if this_channel['update']:
                updated_state = channel.update_channel(this_channel)
                updated_state['update'] = False
                pending_update[i] = updated_state

            # check whether channel is active
            new_world, updated_channel = channel.render_frame(this_channel)

            # Only update state if changes occurred
            if updated_channel is not None:
                pending_update[i] = updated_channel

            # apply channel fade
            self.channelworld[i, :, :, :] = new_world + this_channel['fade']*\
                                             self.channelworld[i, :, :, :]

        # preserve old world if needed for fade effect
        oldworld = None
        if snapshot['fade'] > 0.01:
            oldworld = self.cubeworld.copy()

        # reset cubeworld
        self.cubeworld = np.zeros([3, 10, 10, 10])

        # copy channels together
        for i in range(snapshot['numberOfChannels']):
            if snapshot[i]['IO']:
                brightness = np.clip(snapshot[i]['brightness'], 0, 1)
                self.cubeworld += brightness * self.channelworld[i, :, :, :]

        # check if global effects need to be updated
        if snapshot[9]['update']:
            pending_update[9] = self.update_global_effects(snapshot[9])

        # apply global effect 
        for i in range(snapshot[9]['numberOfEffects']):
            # Update effect state values if needed
            if snapshot[9][i]['update']:
                global_effects = snapshot[9]
                effect_state = self.global_effects[i].return_state()
                for k in range(len(effect_state)):
                    global_effects[i]['params'][4*k:4*k+3] = effect_state[k][:3]
                global_effects[i]['update'] = False
                pending_update[9] = global_effects
            self.cubeworld = self.global_effects[i](self.cubeworld, snapshot[9][i]['params'][3::4])

        # apply global color effect
        if 8 in snapshot[9]:
            if snapshot[9][8]['update']:
                self.cubeworld = self.global_color_effect(self.cubeworld, snapshot[9][8])
                clear_color_update = True
            else:
                self.cubeworld = self.global_color_effect(self.cubeworld)

        # detect whether a oneshot is fired
        if snapshot['oneshot'] > 0:
            print(f"oneshot fired: {snapshot['oneshot']}")
            self.shot_state = snapshot['oneshot']
            self.shot = self.shot_list[int(self.shot_state)]()
            reset_oneshot = True

        if self.shot_state > 0:
            self.cubeworld, counter = self.shot(self.cubeworld)
            if counter <= 0:
                self.shot_state = 0
                self.shot = s_blank()

        # Apply global fade
        if oldworld is not None:
            self.cubeworld += snapshot['fade'] * oldworld

        # adjust global brightness
        self.cubeworld *= snapshot['brightness']

        if pending_update or clear_color_update or reset_oneshot:
            with state.lock:
                for key, value in pending_update.items():
                    state[key] = value
                if clear_color_update:
                    state[9][8]['update'] = False
                if reset_oneshot:
                    state['oneshot'] = 0
            if reset_oneshot:
                try:
                    requests.get("http://localhost:8000/api/update_key/oneshot", timeout=0.1)
                except requests.RequestException:
                    pass


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