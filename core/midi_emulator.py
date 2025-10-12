import tkinter as tk
from tkinter import ttk
import numpy as np
import math
from midi_translation import class_midi_translation
from UltraDict import UltraDict
import time

class RotaryKnob(tk.Canvas):
    def __init__(self, parent, size=50, **kwargs):
        super().__init__(parent, width=size, height=size, **kwargs)
        self.size = size
        self.value = 0  # 0 to 127
        self.callback = None
        
        # Create knob circle
        padding = 5
        self.create_oval(padding, padding, size-padding, size-padding, fill='gray30')
        # Create indicator line
        self.indicator = self.create_line(size/2, size/2, size/2, padding+2, fill='white', width=2)
        
        self.bind('<Button-1>', self.on_click)
        self.bind('<B1-Motion>', self.on_drag)
        
    def set_callback(self, callback):
        self.callback = callback
        
    def on_click(self, event):
        self.last_y = event.y
        
    def on_drag(self, event):
        delta = self.last_y - event.y
        self.last_y = event.y
        
        # Update value (0-127 range)
        self.value = min(127, max(0, self.value + delta))
        
        # Calculate angle based on value (270 degree rotation)
        angle = (self.value / 127) * 270 - 135
        
        # Update indicator line
        center_x = self.size / 2
        center_y = self.size / 2
        radius = (self.size - 10) / 2
        end_x = center_x + radius * math.cos(math.radians(angle))
        end_y = center_y + radius * math.sin(math.radians(angle))
        
        self.coords(self.indicator, center_x, center_y, end_x, end_y)
        
        if self.callback:
            self.callback(self.value)

    def update_indicator(self):
        # Calculate angle based on value (270 degree rotation)
        angle = (self.value / 127) * 270 - 135
        
        # Update indicator line
        center_x = self.size / 2
        center_y = self.size / 2
        radius = (self.size - 10) / 2
        end_x = center_x + radius * math.cos(math.radians(angle))
        end_y = center_y + radius * math.sin(math.radians(angle))
        
        self.coords(self.indicator, center_x, center_y, end_x, end_y)

class MidiControllerEmulator:
    def __init__(self, root):
        self.root = root
        self.root.title("MIDI Controller Emulator")
        self.midi_translation = class_midi_translation()

        # Get screen dimensions and window size
        screen_width = 3840
        screen_height = 2160
        # Wait for window to be created and sized
        root.update_idletasks()
        window_width = root.winfo_width()
        window_height = root.winfo_height()
        
        # Calculate position
        x = (screen_width - window_width) // 2  # Center horizontally
        y = screen_height - window_height - 50   # Bottom of screen with 50px margin
        
        # Set window position
        root.geometry(f'+{x}+{y}')

        # Initialize values arrays (storing 16 values between 0-127)
        self.slider_values = np.zeros(9, dtype=float)
        self.knob_values = np.zeros(8, dtype=float)
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create sliders frame
        self.sliders_frame = ttk.LabelFrame(self.main_frame, text="Faders", padding="10")
        self.sliders_frame.grid(row=0, column=0, padx=10, pady=5)
        
        # Create knobs frame
        self.knobs_frame = ttk.LabelFrame(self.main_frame, text="Knobs", padding="10")
        self.knobs_frame.grid(row=0, column=1, padx=10, pady=5)
        
        # Create sliders
        self.sliders = []
            
        # Create knobs
        self.knobs = []
        for i in range(8):
            # Calculate row and column for 2x4 layout
            row_base = i % 4  # 0-3 for both columns
            col = i // 4     # 0 for first 4 knobs, 1 for last 4
            
            # Create label
            ttk.Label(self.knobs_frame, text=f"Knob {i+1}").grid(row=row_base*3, column=col, pady=5)
            
            # Create knob
            knob = RotaryKnob(self.knobs_frame)
            knob.grid(row=row_base*3 + 1, column=col, padx=10, pady=5)
            knob.set_callback(lambda value, index=i: self.update_knob_value(value, index))
            self.knobs.append(knob)
            
            # Create value label
            value_label = ttk.Label(self.knobs_frame, text="0")
            value_label.grid(row=row_base*3 + 2, column=col, pady=5)
            knob.value_label = value_label
        
        # After the knobs frame setup, add midi buttons frame
        self.midi_buttons_frame = ttk.LabelFrame(self.main_frame, text="MIDI Buttons", padding="10")
        self.midi_buttons_frame.grid(row=0, column=2, padx=10, pady=5)

        # Create midi buttons array (remove state array since we don't need it)
        self.midi_buttons = []

        # Create 3x4 grid of buttons
        for i in range(12):
            row = i // 3        # 0-2 for three rows
            col = i % 3       # 0-3 for four columns
            
            button = ttk.Button(
                self.midi_buttons_frame,
                text=f"M{i+1}",
                width=6,
                command=lambda index=i: self.handle_midi_click(index)
            )
            button.grid(row=row, column=col, padx=5, pady=5)
            self.midi_buttons.append(button)

        self.state_frame = ttk.LabelFrame(self.main_frame, text="State Transition", padding="10")
        self.state_frame.grid(row=1, column=2, padx=10, pady=5)  # Grid below midi_buttons_frame
        
        # Create state A button
        self.state_a_button = ttk.Button(
            self.state_frame,
            text="State A",
            width=8,
            command=lambda: self.handle_state_button('A')
        )
        self.state_a_button.grid(row=0, column=0, padx=5, pady=5)
        
        # Create horizontal crossfade slider
        self.crossfade_slider = ttk.Scale(
            self.state_frame,
            from_=0,
            to=127,
            orient=tk.HORIZONTAL,
            length=150,
            command=self.update_crossfade
        )
        self.crossfade_slider.grid(row=0, column=1, padx=10, pady=5)
        
        # Create state B button
        self.state_b_button = ttk.Button(
            self.state_frame,
            text="State B",
            width=8,
            command=lambda: self.handle_state_button('B')
        )
        self.state_b_button.grid(row=0, column=2, padx=5, pady=5)
        

        # Create sliders frame with more rows for buttons and knobs
        self.sliders_frame = ttk.LabelFrame(self.main_frame, text="Channel Controls", padding="10")
        self.sliders_frame.grid(row=0, column=0, padx=10, pady=5)
        
        # Create arrays for new controls
        self.upper_knobs = []
        self.buttons = []
        self.button_states = np.zeros(9, dtype=int)

        for i in range(9):
            # Create button
            button = ttk.Button(
                self.sliders_frame,
                text="OFF",
                width=6,
                command=lambda index=i: self.toggle_button(index)
            )
            button.grid(row=0, column=i, pady=5)
            self.buttons.append(button)
            
            # Create upper knob
            upper_knob = RotaryKnob(self.sliders_frame)
            upper_knob.grid(row=1, column=i, padx=10, pady=5)
            upper_knob.set_callback(lambda value, index=i: self.update_upper_knob_value(value, index))
            self.upper_knobs.append(upper_knob)
            
            # Create upper knob value label
            upper_value_label = ttk.Label(self.sliders_frame, text="0")
            upper_value_label.grid(row=2, column=i, pady=5)
            upper_knob.value_label = upper_value_label

            # Create slider label (moved to row 3)
            ttk.Label(self.sliders_frame, text=f"Fader {i+1}").grid(row=3, column=i, pady=5)
            
            # Create slider (moved to row 4)
            slider = ttk.Scale(
                self.sliders_frame,
                from_=127,
                to=0,
                orient=tk.VERTICAL,
                length=200,
                command=lambda value, index=i: self.update_slider_value(value, index)
            )
            slider.grid(row=4, column=i, padx=10, pady=5)
            self.sliders.append(slider)
            
            # Create slider value label (moved to row 5)
            value_label = ttk.Label(self.sliders_frame, text="0")
            value_label.grid(row=5, column=i, pady=5)
            slider.value_label = value_label
        
        self.state = UltraDict(name='state')  # Add shared state
        # map initial values for brightness and fade

        self.update_fixed_midi()

    def update_fixed_midi(self):
        for i in range(8):
            # self.slider_values[i] = self.state.get(i, {}).get('brightness', 0)
            # self.upper_knobs[i] = self.state.get(i, {}).get('fade', 0)
            # self.button_states[i] = self.state.get(i, {}).get('IO', 0)

            brightness = self.state.get(i, {}).get('brightness', 0)
            brightness = int(round(brightness * 127))
            self.slider_values[i] = brightness

            self.sliders[i].value_label.config(text=str(brightness))
            self.sliders[i].set(brightness)

            fade = self.state.get(i, {}).get('fade', 0)
            fade = int(round(fade * 127))
            self.upper_knobs[i].value = fade
            self.upper_knobs[i].value_label.config(text=str(fade))

            IO = self.state.get(i, {}).get('IO', 0)
            self.button_states[i] = IO
            self.buttons[i].configure(
                text="ON" if IO else "OFF"
            )


        brightness = self.state['brightness']
        brightness = int(round(brightness * 127))
        self.slider_values[8] = brightness

        self.sliders[8].value_label.config(text=str(brightness))
        self.sliders[8].set(brightness)

        fade = self.state['fade']
        fade = int(round(fade * 127))
        self.upper_knobs[8].value = fade
        self.upper_knobs[8].value_label.config(text=str(fade))

        IO = self.state['IO']
        self.button_states[8] = IO
        self.buttons[8].configure(
            text="ON" if IO else "OFF"
        )

        self.setup_midi_monitor()


    def setup_midi_monitor(self):
        def check_midi_update():
            with self.state.lock:
                if self.state['midi_update'] == 1:
                    self.state['midi_update'] = 0  # Reset flag
                    self.update_controls_from_midi()
            self.root.after(100, check_midi_update)  # Check every 100ms
        
        check_midi_update()

    def update_controls_from_midi(self):
        # Get current context from state
        channel, index = self.state['context']
        if channel != 9 and channel >= self.state['numberOfChannels']:
            print(f"Invalid channel: {channel}")
            return
        if index != 9 and index >= self.state[channel]['numberOfEffects']:
            print(f"Invalid index: {index}")
            return
            
        for i in range(8):
            self.knob_values[i] = 0

        if channel <= 9:
            try:
                params = self.state[channel][index]['params']
                print(params)
                print(len(params) // 4)
                for i in range(len(params) // 4):
                    midi_value = params[i * 4 + 3]
                    if isinstance(midi_value, str):
                        self.knob_values[i] = 0
                    else:
                        self.knob_values[i] = int(round(midi_value * 127))
            except (KeyError, IndexError) as e:
                print(f"Error updating controls: {e}")

        elif channel == 10:
            try:
                for i in range(8):
                    midi_value = self.state['s2l_values'][i] if i < 4 else self.state['s2l_thresholds'][i-4]
                    self.knob_values[i] = int(round(midi_value * 127))
                    # Update the knob UI
            except (KeyError, IndexError) as e:
                print(f"Error updating S2L controls: {e}")

        # Update the knob UI
        for i in range(8):
            self.knobs[i].value = self.knob_values[i]
            self.knobs[i].value_label.config(text=str(self.knob_values[i]))
            self.knobs[i].update_indicator()
        self.update_fixed_midi()

    def toggle_button(self, index):
        self.button_states[index] = 127 if self.button_states[index] == 0 else 0
        self.buttons[index].configure(
            text="ON" if self.button_states[index] else "OFF"
        )
        self.midi_translation.update_fixed(index, 'IO', self.button_states[index])
        # print(f"Button {index} state: {self.button_states[index]}")

    def update_slider_value(self, value, index):
        self.slider_values[index] = int(round(float(value)))
        # print(f"Slider {index} value: {self.slider_values[index]}")
        self.midi_translation.update_fixed(index, 'brightness', self.slider_values[index])
        self.sliders[index].value_label.config(text=str(self.slider_values[index]))
        # print(f"Slider Values: {self.slider_values}")

    def update_upper_knob_value(self, value, index):
        rounded_value = int(round(float(value)))
        # print(f"Upper Knob {index} value: {rounded_value}")
        self.upper_knobs[index].value_label.config(text=str(rounded_value))
        # Fix: Pass rounded_value instead of the RotaryKnob object
        self.midi_translation.update_fixed(index, 'fade', rounded_value)

    def update_knob_value(self, value, index):
        self.knob_values[index] = int(round(float(value)))
        # print(f"Knob {index} value: {self.knob_values[index]}")
        self.midi_translation.update_context(0, index, self.knob_values[index])
        self.knobs[index].value_label.config(text=str(self.knob_values[index]))

    def handle_state_button(self, state):
        """Handle state A/B button clicks"""
        print(f"State {state} button clicked")
        self.midi_translation.save_state(state)
        # Add your state handling logic here

    def update_crossfade(self, value):
        """Handle crossfade slider updates"""
        value = int(float(value))
        self.midi_translation.crossfade(value)
        print(f"Crossfade value: {value}")
        # Add your crossfade handling logic here
            # print(f"Knob Values: {self.knob_values}")

    def handle_midi_click(self, index):
        """Handle MIDI button click"""
        # print(f"MIDI Button {index + 1} clicked")
        self.midi_translation.oneshot(index + 1)

def main():
    root = tk.Tk()
    app = MidiControllerEmulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()