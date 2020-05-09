import numpy as np

labels = np.full((21, 8, 8), 'empty')
labels[1:, 0, 0] = 'close'

#  1 - 5 (inklusiv): channel 1
#  6 -10 (inklusiv): channel 2
# 11 -15 (inklusiv): channel 3
# 16 -20 (inklusiv): channel 4

# add generators
for i in [2, 7, 12, 17]:
    labels[i, 1, 1] = 'blank'
    labels[i, 1, 2] = 'random'
    labels[i, 1, 3] = 'planes'
    labels[i, 1, 4] = 'cube'
    labels[i, 1, 5] = 'wave'
    labels[i, 1, 6] = 'growing sphere'
    labels[i, 1, 7] = 'squares'
    labels[i, 1, 7] = 'random'

    labels[i, 2, 0] = 'trees'
    labels[i, 2, 1] = 'rising square'
    labels[i, 2, 2] = 'planes (falling)'
    labels[i, 2, 3] = 'growing face'
    labels[i, 2, 4] = 'snake'
    labels[i, 2, 5] = 'sound sphere'
    labels[i, 2, 6] = 'sphere'
    labels[i, 2, 7] = 'shooting star'

    labels[i, 3, 0] = 'rotating plane'
    labels[i, 3, 1] = 'random lines'
    labels[i, 3, 2] = 'random cross'
    labels[i, 3, 3] = 'rain'
    labels[i, 3, 4] = 'orbiter (x)'
    labels[i, 3, 5] = 'orbiter (y)'
    labels[i, 3, 6] = 'orbiter (z)'
    labels[i, 3, 7] = 'pyramid'

    labels[i, 4, 0] = 'pyramid (upside down)'
    labels[i, 4, 1] = 'in and out'
    labels[i, 4, 2] = 'growing corner'
    labels[i, 4, 3] = 'falling '
    labels[i, 4, 4] = 'drop'
    labels[i, 4, 5] = 'dark sphere'
    labels[i, 4, 6] = 'cut'
    labels[i, 4, 7] = 'pyramid'

    labels[i, 5, 0] = 'cube edges'
    labels[i, 5, 1] = 'corner'
    labels[i, 5, 2] = 'corner grow'
    labels[i, 5, 3] = 'columns'
    labels[i, 5, 4] = 'circles'
    labels[i, 5, 5] = 'grow'
    labels[i, 5, 6] = 'empty'
    labels[i, 5, 7] = 'empty'

    labels[i, 6, 0] = 'a_lines'
    labels[i, 6, 1] = 'a_multi_cube_edges'
    labels[i, 6, 2] = 'a_pulsating'
    labels[i, 6, 3] = 'a_orbot'
    labels[i, 6, 4] = 'a_random_cubes'
    labels[i, 6, 5] = 'a_squares_cut'
    labels[i, 6, 6] = 'a_testbot'
    labels[i, 6, 7] = 'empty'

# effect
for i in [3,4,5, 8,9,10, 13,14,15, 18,19,20]:
    labels[i, 1, 0] = 'e_blank'
