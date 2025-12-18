import time as time
from rtmidi.midiutil import open_midiinput, open_midioutput
from midi_translation import class_midi_translation

class class_fighter:
    def __init__(self, state):
        """initializes the MIDI fighter"""
        self.midi_inputs = []
        self.midi_outputs = []
        
        # Try to open first Fighter
        try:
            midiin, portname_in = open_midiinput('Fighter')
            midiin.set_callback(self.event)
            self.midi_inputs.append(midiin)
            
            midiout, portname_out = open_midioutput('Fighter')
            self.midi_outputs.append(midiout)
            print(f"Attached to Fighter: {portname_in}")
        except:
            print("No Fighter found")

        # Try to open second Fighter (if available)
        try:
            # Note: open_midiinput might return the same port if not careful, 
            # but usually it finds the first matching. 
            # To properly support multiple, we'd need to iterate ports.
            # For now, we'll assume the user might have a specific setup or this is a placeholder.
            # A more robust way is to list ports and open by index.
            pass 
        except:
            pass

        self.midi_translation = class_midi_translation(state)
        
        # Mapping: Column-major
        # Col 0: 0, 4, 8, 12
        # Col 1: 1, 5, 9, 13
        # ...
        self.fighter_mapping = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
        
        # Bank state for each column (0 = params 0-3, 1 = params 4-7)
        self.column_banks = [0, 0, 0, 0]
        
        # Colors for each column (White, Cyan, Yellow, Pink)
        # These correspond to the ContextSelector colors in the frontend
        self.column_colors = [127, 60, 20, 95]

    def event(self, event, data=None):
        message, deltatime = event
        # print(message)

        # Handle Knobs (CC)
        if message[0] == 176:
            if message[1] in self.fighter_mapping:
                idx = self.fighter_mapping.index(message[1])
                col = idx // 4
                row = idx % 4
                
                # Calculate parameter index based on bank
                # Bank 0: params 0-3
                # Bank 1: params 4-7
                param_idx = row + (self.column_banks[col] * 4)
                
                self.midi_translation.update_context(col, param_idx, message[2])

        # Handle Buttons (Note On) - Switch Banks
        # Top button (Row 0) -> Bank 0
        # Bottom button (Row 3) -> Bank 1
        elif message[0] == 144 and message[2] > 0: # Note On with velocity > 0
            if message[1] in self.fighter_mapping:
                idx = self.fighter_mapping.index(message[1])
                col = idx // 4
                row = idx % 4
                
                if row == 0: # Top button
                    self.column_banks[col] = 0
                elif row == 3: # Bottom button
                    self.column_banks[col] = 1

    def update(self):
        # Update feedback for all columns
        with self.midi_translation.state.lock:
            context = self.midi_translation.state['context']
            
            for col in range(4):
                channel_idx = context[col][0]
                element_idx = context[col][1]
                
                # Fetch parameters for the element in this context slot
                params = []
                try:
                    if channel_idx < 10: # Normal channel
                        channel = self.midi_translation.state[channel_idx]
                        if element_idx == 9: # Generator
                            if 'params' in channel[9]:
                                params = channel[9]['params']
                        elif element_idx < channel['numberOfEffects']: # Effect
                            if 'params' in channel[element_idx]:
                                params = channel[element_idx]['params']
                except Exception:
                    pass

                # Determine offset based on bank
                bank_offset = self.column_banks[col] * 4
                col_color = self.column_colors[col]
                
                # Update the 4 knobs in this column
                for row in range(4):
                    fighter_idx = col * 4 + row
                    cc_num = self.fighter_mapping[fighter_idx]
                    
                    # Target parameter index
                    param_idx = bank_offset + row
                    
                    # Extract value (every 4th element is the MIDI value)
                    val = 0
                    if params and (param_idx * 4 + 3) < len(params):
                        val = params[param_idx * 4 + 3]
                    
                    midi_val = int(val * 127)
                    
                    # Send to all outputs
                    for midiout in self.midi_outputs:
                        # Send Value (CC Ch 1)
                        midiout.send_message([176, cc_num, midi_val])
                        
                        # Send Color/Animation (CC Ch 2 - 177)
                        # We light up the active bank button with the column color
                        # Row 0 is Bank 0 selector, Row 3 is Bank 1 selector
                        led_color = 0 # Off by default
                        
                        if row == 0 and self.column_banks[col] == 0:
                            led_color = col_color
                        elif row == 3 and self.column_banks[col] == 1:
                            led_color = col_color
                        
                        # Send color to switch (using 177 as per previous code, 
                        # though Note On is standard for switches, 177 might be for ring color or custom mapping.
                        # I'll send both to be safe/robust for different configs)
                        midiout.send_message([177, cc_num, led_color])
                        
                        # Also send Note On for switch LED if 177 doesn't work for switches
                        # (Note On 144, Note = cc_num, Vel = color)
                        # Only send if color > 0 to avoid turning off if not intended, 
                        # or send 0 to turn off.
                        midiout.send_message([144, cc_num, led_color])
