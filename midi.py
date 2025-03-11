import numpy as np
import requests

class class_midi:

    def __init__(self, state):
        self.state = state
        self.midi_values = [0, 0, 0, 0]

    def update_midi(self):
        channel = self.state['context'][0]
        index = self.state['context'][1]
        print('channel', channel)
        print('index', index)
        for i in range(4):
            self.midi_values[i] = self.state['midi_values'][i + 1]
        if channel <= 9:
            this_channel = self.state[channel]
            if index == 9:
                generator = this_channel['generator']
                for i in range(len(generator['params'])//4):
                    generator['params'][i*4+3]  = self.midi_values[i]
                generator['update'] = 1
            elif index == 10:
                this_channel['IO'] = self.midi_values[0]
                this_channel['brightness'] = self.midi_values[1]
                this_channel['fade'] = self.midi_values[2]
            else:
                effect = this_channel['effects'][index]
                for i in range(len(effect['params'])//4):
                    effect['params'][i * 4 + 3] = self.midi_values[i]
                effect['update'] = 1
            this_channel['update'] = 1
            self.state[channel] = this_channel
            self.notify_frontend("This is an important message from the backend")
        # THIS IS NOT WORKING YET
        if channel == 10:
            print('channel 10')
            # Get current values
            current_values = list(self.state['s2l_values'])  # Make a copy of current values
            print('current_values', current_values)
            
            # Update specific index
            for i in range(4):
                current_values[i] = self.midi_values[i] 
            
            print('updated current_values', current_values
                  )
            # Update state with new list
            self.state['s2l_values'] = current_values
            
            # Notify frontend of the change
            self.notify_frontend({
                "type": "s2l_update",
                "values": current_values
            })
            
            print('Updated s2l_values:', self.state['s2l_values'])

    def notify_frontend(self, message):
        data = {
            "type": "midi_update",
            "data": message
        }
        requests.post(
            "http://localhost:8000/api/stream", 
            json = data, 
            headers = {"Content-Type": "application/json"}
        )
