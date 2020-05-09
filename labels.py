import numpy as np

labels = np.full((20, 8, 8), 'empty')
labels[1:, 0, 0] = 'close'

#  1 - 5 (inklusiv): channel 1
#  6 -10 (inklusiv): channel 2
# 11 -15 (inklusiv): channel 3
# 16 -20 (inklusiv): channel 4

# add generators
for i in [2, 7, 12, 17]:
    labels[i, 1, 0] = 'g_blank'
    labels[i, 1, 0] = 'g_random'

# effect
for i in [3,4,5, 8,9,10, 13,14,15, 18,19,20]:
    labels[i, 1, 0] = 'e_blank'
