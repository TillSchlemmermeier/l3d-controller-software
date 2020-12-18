import numpy as np


# load presets
preset_labels = []

with open('presets.dat', 'r') as file:
    presets = file.readlines()

for p in presets:
    preset_labels.append(p.split()[0])



# variable for launchpad text labels

# number from global array defines 'layer':
#      0            : closed menu
#  1 - 5 (inklusiv) : channel 1
#  6 -10 (inklusiv) : channel 2
# 11 -15 (inklusiv) : channel 3
# 16 -20 (inklusiv) : channel 4

# create a default/empty string
# length given by for loop
default = ''
for i in range(150):
    default += ' '

# create empty numpy aray
labels = np.full((21, 8, 8), default)
labels[:,:,:]= ''
# add close labels except for first 'layer'
labels[1:, 0, 0] = 'close'

# add presets

for i in [1, 6, 11, 16]:
    counter = 0

    # first row
    for j in range(1, 8):
        if counter < len(preset_labels):
            labels[i, 0, j] = preset_labels[counter]

        counter += 1

    # second row
    for j in range(0, 8):
        if counter < len(preset_labels):
            labels[i, 1, j] = preset_labels[counter]

        counter += 1

    #third grow
    for j in range(0, 8):
        if counter < len(preset_labels):
            labels[i, 2, j] = preset_labels[counter]

        counter += 1

# add generators
for i in [2, 7, 12, 17]:
    labels[i, 0, 1] = 'blank'
    labels[i, 0, 2] = 'random'
    labels[i, 0, 3] = 'frame'

# add effect
for i in [3,4,5, 8,9,10, 13,14,15, 18,19,20]:
    labels[i, 0, 1] = 'blank'
    labels[i, 0, 2] = 'rainbow'
    labels[i, 0, 3] = 'static\ncolor'
    labels[i, 0, 4] = 'gradient'
    labels[i, 0, 5] = 'new\ngradient'
    labels[i, 0, 6] = 'palettes'
    labels[i, 0, 7] = 'red\nyellow'

    labels[i, 1, 0] = 'S2L'
    labels[i, 1, 1] = 'tremolo'
    labels[i, 1, 2] = 'rare\nstrobo'
    labels[i, 1, 3] = 'bright\nosci'
    labels[i, 1, 4] = 'mean'
    labels[i, 1, 5] = 'mean\n(vertical)'
    labels[i, 1, 6] = 'random\nbrightness'
    labels[i, 1, 7] = 'squared'

    labels[i, 2, 0] = 'rotate\nblack/color'
    labels[i, 2, 1] = 'rotate\nblack/white'
    labels[i, 2, 2] = 'rotate\nblack/orange'
    labels[i, 2, 3] = 'rotation'
    labels[i, 2, 4] = 'rotating\nrainbow'
    labels[i, 2, 5] = 'radial\ngradient'
    labels[i, 2, 6] = 'sound\ncolor'
    labels[i, 2, 7] = 'mean\nup-down'

    labels[i, 3, 0] = 'outer\nshadow'
    labels[i, 3, 1] = 'sound\ngradient'
#    labels[i, 3, 1] = 'growing\nsphere'
#    labels[i, 3, 2] = 'outer\nshadow'
#    labels[i, 3, 3] = 'zoom'


#    labels[i, 4, 0] = 'prod\nhue'
#    labels[i, 4, 1] = 'prod\nsaturation'
#    labels[i, 4, 2] = 'fade2blue'
