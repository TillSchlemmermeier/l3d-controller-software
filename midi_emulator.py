import tkinter as tk
from tkinter import ttk
import numpy as np
import math

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

class MidiControllerEmulator:
    def __init__(self, root):
        self.root = root
        self.root.title("MIDI Controller Emulator")
        
        # Initialize values arrays (storing 16 values between 0-127)
        self.slider_values = np.zeros(8, dtype=int)
        self.knob_values = np.zeros(8, dtype=int)
        
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
        for i in range(8):
            # Create label
            ttk.Label(self.sliders_frame, text=f"Fader {i+1}").grid(row=0, column=i, pady=5)
            
            # Create slider
            slider = ttk.Scale(
                self.sliders_frame,
                from_=127,
                to=0,
                orient=tk.VERTICAL,
                length=200,
                command=lambda value, index=i: self.update_slider_value(value, index)
            )
            slider.grid(row=1, column=i, padx=10, pady=5)
            self.sliders.append(slider)
            
            # Create value label
            value_label = ttk.Label(self.sliders_frame, text="0")
            value_label.grid(row=2, column=i, pady=5)
            slider.value_label = value_label
            
        # Create knobs
        self.knobs = []
        for i in range(8):
            # Create label
            ttk.Label(self.knobs_frame, text=f"Knob {i+1}").grid(row=0, column=i, pady=5)
            
            # Create knob
            knob = RotaryKnob(self.knobs_frame)
            knob.grid(row=1, column=i, padx=10, pady=5)
            knob.set_callback(lambda value, index=i: self.update_knob_value(value, index))
            self.knobs.append(knob)
            
            # Create value label
            value_label = ttk.Label(self.knobs_frame, text="0")
            value_label.grid(row=2, column=i, pady=5)
            knob.value_label = value_label

    def update_slider_value(self, value, index):
        self.slider_values[index] = int(float(value))
        self.sliders[index].value_label.config(text=str(self.slider_values[index]))
        print(f"Slider Values: {self.slider_values}")
        
    def update_knob_value(self, value, index):
        self.knob_values[index] = int(value)
        self.knobs[index].value_label.config(text=str(self.knob_values[index]))
        print(f"Knob Values: {self.knob_values}")

def main():
    root = tk.Tk()
    app = MidiControllerEmulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()