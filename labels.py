import numpy as np

labels = np.full((21, 8, 8), '              ')
labels[1:, 0, 0] = 'close'

#  1 - 5 (inklusiv): channel 1
#  6 -10 (inklusiv): channel 2
# 11 -15 (inklusiv): channel 3
# 16 -20 (inklusiv): channel 4

# add generators
for i in [2, 7, 12, 17]:
    labels[i, 0, 1] = 'blank'
    labels[i, 0, 2] = 'random'
    labels[i, 0, 3] = 'planes'
    labels[i, 0, 4] = 'cube'
    labels[i, 0, 5] = 'wave'
    labels[i, 0, 6] = 'growing\nsphere'
    labels[i, 0, 7] = 'squares'
    labels[i, 0, 7] = 'random'

    labels[i, 1, 0] = 'trees'
    labels[i, 1, 1] = 'rising square'
    labels[i, 1, 2] = 'planes (falling)'
    labels[i, 1, 3] = 'growing face'
    labels[i, 1, 4] = 'snake'
    labels[i, 1, 5] = 'sound sphere'
    labels[i, 1, 6] = 'sphere'
    labels[i, 1, 7] = 'shooting star'

    labels[i, 2, 0] = 'rotating plane'
    labels[i, 2, 1] = 'random lines'
    labels[i, 2, 2] = 'random cross'
    labels[i, 2, 3] = 'rain'
    labels[i, 2, 4] = 'orbiter (x)'
    labels[i, 2, 5] = 'orbiter (y)'
    labels[i, 2, 6] = 'orbiter (z)'
    labels[i, 2, 7] = 'pyramid'

    labels[i, 3, 0] = 'pyramid (upside down)'
    labels[i, 3, 1] = 'in and out'
    labels[i, 3, 2] = 'growing corner'
    labels[i, 3, 3] = 'falling '
    labels[i, 3, 4] = 'drop'
    labels[i, 3, 5] = 'dark sphere'
    labels[i, 3, 6] = 'cut'
    labels[i, 3, 7] = 'pyramid'

    labels[i, 4, 0] = 'cube edges'
    labels[i, 4, 1] = 'corner'
    labels[i, 4, 2] = 'corner grow'
    labels[i, 4, 3] = 'columns'
    labels[i, 4, 4] = 'circles'
    labels[i, 4, 5] = 'grow'
    labels[i, 4, 6] = 'empty'
    labels[i, 4, 7] = 'empty'

    labels[i, 5, 0] = 'a_lines'
    labels[i, 5, 1] = 'a_multi_cube_edges'
    labels[i, 5, 2] = 'a_pulsating'
    labels[i, 5, 3] = 'a_orbot'
    labels[i, 5, 4] = 'a_random_cubes'
    labels[i, 5, 5] = 'a_squares_cut'
    labels[i, 5, 6] = 'a_testbot'
    labels[i, 5, 7] = 'empty'

# effect
for i in [3,4,5, 8,9,10, 13,14,15, 18,19,20]:
    labels[i, 0, 1] = 'blank'
    labels[i, 0, 2] = 'raindbow'
    labels[i, 0, 3] = 'static color'
    labels[i, 0, 4] = 'gradient'
    labels[i, 0, 5] = 'new gradient'
    labels[i, 0, 6] = 'palettes'
    labels[i, 0, 7] = 'red yellow'

    labels[i, 1, 0] = 'S2L'
    labels[i, 1, 1] = 'tremolo'
    labels[i, 1, 2] = 'rare strobo'
    labels[i, 1, 3] = 'blur'
    labels[i, 1, 4] = 'bright osci'
    labels[i, 1, 5] = 'mean'
    labels[i, 1, 6] = 'mean vertical'
    labels[i, 1, 7] = 'random brightness'

    labels[i, 2, 0] = 'rotate black/color'
    labels[i, 2, 1] = 'rotate black/white'
    labels[i, 2, 2] = 'rotate black/ornage'
    labels[i, 2, 3] = 'rotation'

    labels[i, 3, 0] = 'cut cube'
    labels[i, 3, 1] = 'growing sphere'
    labels[i, 3, 2] = 'outer shadow'

    labels[i, 4, 0] = 'prod hue'
    labels[i, 4, 1] = 'prod saturation'
    labels[i, 4, 2] = 'fade2blue'
