# L3D Cube 3.0

## Parameterset / Global Variable

In the following, the global parameters are listed. Default values are given in brackets, if there are some.

- 0 - 9: global parameters
  - 0 : on/off (0)
  - 1 : brightness (50)
  - 2 : fade (0)
  - 3 : channel brightness limiter (200)
- 10 - 10: sound2light
- 20 - 39: channel settings
  - 20 : preset channel 1
  - 21 : generator channel 1
  - 22 : 1. effect channel 1
  - 23 : 2. effect channel 1
  - 24 : 3. effect channel 1
- 40 - 69: parameters for channel 1
  - 40 : on/off (0)
  - 41 : brightness
  - 42 : fade
- 70 - 99: parameters for channel 2
  - 70 : on/off (0)
  - 71 : brightness
  - 72 : fade
- 100 - 129: parameters for channel 3
  - 100 : on/off (0)
  - 101 : brightness
  - 102 : fade
- 130 - 159: parameters for channel 4
  - 130 : on/off (0)
  - 131 : brightness
  - 132 : fade

## Testing for rendering engine

The script 'test_rendering_engine.py' starts the frame renderer in a thread to check for errors. Check the log file for output.
