
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
|        4 | state of launchpad       | 0-19   | 0
|        5 | autopilot                | 0,1    | 1
|        6 | autopilot time           | 0-1    | 0.1
| 10 -  19 | **sound2light**
|       10 | value 1                  | 0-X    | 0
|       11 | value 2                  | 0-X    | 0
|       12 | value 3                  | 0-X    | 0
|       13 | value 4                  | 0-X    | 0
|       14 | thresh 1                 | 0-X    | 0
|       15 | thresh 2                 | 0-X    | 0
|       16 | thresh 3                 | 0-X    | 0
|       17 | thresh 4                 | 0-X    | 0
|       18 | normalize                | 0-X    | 0
|       19 | gain                     | 0-X    | 0
| 20 -  39 | **channel settings**
|       20 | generator channel 1      | 0-255  | 0
|       21 | effect 1 channel 1       | 0-255  | 0
|       22 | effect 2 channel 1       | 0-255  | 0
|       23 | effect 3 channel 1       | 0-255  | 0
|       25 | generator channel 2      | 0-255  | 0
|       26 | effect 1 channel 2       | 0-255  | 0
|       27 | effect 2 channel 2       | 0-255  | 0
|       28 | effect 3 channel 2       | 0-255  | 0
|       30 | generator channel 3      | 0-255  | 0
|       31 | effect 1 channel 3       | 0-255  | 0
|       32 | effect 2 channel 3       | 0-255  | 0
|       33 | effect 3 channel 3       | 0-255  | 0
|       35 | generator channel 4      | 0-255  | 0
|       36 | effect 1 channel 4       | 0-255  | 0
|       37 | effect 2 channel 4       | 0-255  | 0
|       38 | effect 3 channel 4       | 0-255  | 0
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
|200 - 219 | system parameters
|      200 | selection menu  (pad)    | 0-21,22,23,24   | 0
|      201 | selection menu  (fighter, ch 1)    | 0-4   | 0
|      202 | selection menu  (fighter, ch 2)    | 0-4   | 0
|      203 | selection menu  (fighter, ch 3)    | 0-4   | 0
|      204 | selection menu  (fighter, ch 4)    | 0-5   | 0
|220 - 229 | one shots
|      220 | one shot state
|230 - ??? | global effect parameters
|      230 | global effects menu trigger
|      231 | global effect 1
|      232 | global effect 1
|      233 | global effect 1
|234 - 237 | global effect 1 parameters
|238 - 241 | global effect 2 parameters
|242 - 245 | global effect 3 parameters

## Testing for rendering engine

The script 'test_rendering_engine.py' starts the frame renderer in a thread to check for errors. Check the log file for output. The global variable is inside *global_parameter_module.py* and imported by any thread, which is using it.


## list of label
| 0 | generator 1 name
| 1-4 | generator 1 params
| 5 | effect 1 name
| 6-9 | effect params
| 10 | effect 2 name
| 11-14 | effect params
| 15 | effect 3 name
| 16-19 | effect params
| 20 - 39 | channel 2
| 40 - 59 | channel 3
| 60 - 79 | channel 4
| 80 - 95 | global effects labels

## Installation
sudo apt-get install python3-pip
sudo apt install gfortran
sudo apt install ipython3
apt-get install python3-pyserial
apt-get install python3-PyAudio
apt-get install PyQt5
apt-get install python-rtmidi
apt-get install libasound-dev
pip3 install numpy
pip3 install scipy
pip3 install matplotlib
pip3 install pyqtgraph
pip3 install PyOpenGL
sudo apt install python3-pyqt4.qtopengl
sudo apt install python3-tk
sudo pip3 install sklearn

git clone https://github.com/TillSchlemmermeier/l3d-controller-software
cd l3d-controller-software/
git checkout dev_3.0

make
cd generators
make
cd ./effects
f2py3 -c -m gen_outer_shadow_f e_outer_shadow_f.f90

sudo usermod -a -G dialout $USER
reboot

python3.8 main.py
