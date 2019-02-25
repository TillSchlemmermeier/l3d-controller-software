
# L3D Cube 3.0

Readme for the L3D Cube software 3.0.

## Content

- Thread and Gui Structure
- Global Variable
- Testing of rendering engine

## Thread and Gui Structure

Here, a rough overview of the thread structure and the signal flow is presented. The main routine starts the QT Gui, which will start the corresponding processes for the MIDI devices, the rendering engine and all other threads.

The rendering thread contains a loop, which will call the rendering engine each time. This will produce a frame everytime it is called based on the information stored in the global variable. The MIDI thread contains the MIDI classes for all devices. Their callbacks will process any incomming MIDI messages and will pass them to the correct place.

main() -> MainWindow() -> MainWindow.start_Renderer() -> midi Thread / rendering Thread

midi Thread -> MidiDevice() -> MidiInputHandler() -> GlobalParameterHandler()

## Global Variable

In the following, the global parameters are listed. Default values are given in brackets, if there are some. Since some channels are used for selecting settings like an generator or an effect, integer numbers from 0 to 255 are used (even though they are stored as floats) for those, an floats from zero to one for all passed parameters, like brightness or fade. In the following, all parameters, default values and type of number are listed.

| channel  | description              | values | default value
| ------:  | :-------                 | ------:| -------:
|   0 -  9 | **global parameters**
|        0 | on/off                   | 0,1    | 0  
|        1 | brightness               | 0-1    | 0.5
|        2 | fade                     | 0-1    | 0.0
|        3 | brightness limiter       | 0-1    | 0.8
| 10 -  19 | **sound2light**
| 20 -  39 | **channel settings**
|       20 | generator channel 1      | 0-255  | 0
|       21 | effect 1 channel 1       | 0-255  | 0
|       22 | effect 1 channel 1       | 0-255  | 0
|       23 | effect 1 channel 1       | 0-255  | 0
|       25 | generator channel 2      | 0-255  | 0
|       26 | effect 1 channel 2       | 0-255  | 0
|       27 | effect 1 channel 2       | 0-255  | 0
|       28 | effect 1 channel 2       | 0-255  | 0
|       30 | generator channel 3      | 0-255  | 0
|       31 | effect 1 channel 3       | 0-255  | 0
|       32 | effect 1 channel 3       | 0-255  | 0
|       33 | effect 1 channel 3       | 0-255  | 0
|       35 | generator channel 4      | 0-255  | 0
|       36 | effect 1 channel 4       | 0-255  | 0
|       37 | effect 1 channel 4       | 0-255  | 0
|       38 | effect 1 channel 4       | 0-255  | 0
| 40 -  69 | **parameters channel 1**
|       40 | on/off                   | 0,1    | 0  
|       41 | brightness               | 0-1    | 1.0
|       42 | fade                     | 0-1    | 0.0
|       43 | strobo                   | 0-1    | 0.0
|       45 | generator parameter 1    | 0-1    | 0.0
|       46 | generator parameter 2    | 0-1    | 0.0
|       47 | generator parameter 3    | 0-1    | 0.0
|       48 | generator parameter 4    | 0-1    | 0.0
|       50 | effect 1 parameter 1     | 0-1    | 0.0
|       51 | effect 1 parameter 2     | 0-1    | 0.0
|       52 | effect 1 parameter 3     | 0-1    | 0.0
|       53 | effect 1 parameter 4     | 0-1    | 0.0
|       55 | effect 2 parameter 1     | 0-1    | 0.0
|       56 | effect 2 parameter 2     | 0-1    | 0.0
|       57 | effect 2 parameter 3     | 0-1    | 0.0
|       58 | effect 2 parameter 4     | 0-1    | 0.0
|       60 | effect 3 parameter 1     | 0-1    | 0.0
|       61 | effect 3 parameter 2     | 0-1    | 0.0
|       62 | effect 3 parameter 3     | 0-1    | 0.0
|       63 | effect 3 parameter 4     | 0-1    | 0.0
| 70 -  99 | **parameters channel 2**
|100 - 129 | **parameters channel 3**
|130 - 159 | **parameters channel 4**

## Testing for rendering engine

The script 'test_rendering_engine.py' starts the frame renderer in a thread to check for errors. Check the log file for output. The global variable is inside *global_parameter_module.py* and imported by any thread, which is using it.
