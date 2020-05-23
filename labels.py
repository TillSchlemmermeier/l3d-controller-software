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

print(len(preset_labels), preset_labels)
for i in [1, 6, 11, 16]:
    counter = 0
    for j in range(1, 8):
        if counter < len(preset_labels):
            print(j, counter)
            labels[i, 0, j] = preset_labels[counter]

        counter += 1



# add generators
for i in [2, 7, 12, 17]:
    labels[i, 0, 1] = 'blank'
    labels[i, 0, 2] = 'random'
    labels[i, 0, 3] = 'planes'
    labels[i, 0, 4] = 'cube'
    labels[i, 0, 5] = 'wave'
    labels[i, 0, 6] = 'growing\nsphere'
    labels[i, 0, 7] = 'squares'

    labels[i, 1, 0] = 'trees'
    labels[i, 1, 1] = 'rising\nsquare'
    labels[i, 1, 2] = 'planes\n(falling)'
    labels[i, 1, 3] = 'growing\nface'
    labels[i, 1, 4] = 'snake'
    labels[i, 1, 5] = 'sound\nsphere'
    labels[i, 1, 6] = 'sphere'
    labels[i, 1, 7] = 'shooting\nstar'

    labels[i, 2, 0] = 'rotating\nplane'
    labels[i, 2, 1] = 'random\nlines'
    labels[i, 2, 2] = 'random\ncross'
    labels[i, 2, 3] = 'rain'
    labels[i, 2, 4] = 'orbiter (x)'
    labels[i, 2, 5] = 'orbiter (y)'
    labels[i, 2, 6] = 'orbiter (z)'
    labels[i, 2, 7] = 'pyramid'

    labels[i, 3, 0] = 'pyramid\n(upside)'
    labels[i, 3, 1] = 'in and\nout'
    labels[i, 3, 2] = 'growing\ncorner'
    labels[i, 3, 3] = 'falling '
    labels[i, 3, 4] = 'drop'
    labels[i, 3, 5] = 'dark\nsphere'
    labels[i, 3, 6] = 'cut'
    labels[i, 3, 7] = 'empty'

    labels[i, 4, 0] = 'cube edges'
    labels[i, 4, 1] = 'corner'
    labels[i, 4, 2] = 'corner\ngrow'
    labels[i, 4, 3] = 'columns'
    labels[i, 4, 4] = 'circles'
    labels[i, 4, 5] = 'grow'
    labels[i, 4, 6] = 'empty'
    labels[i, 4, 7] = 'empty'

    labels[i, 5, 0] = 'a_lines'
    labels[i, 5, 1] = 'a_multi\ncube_edges'
    labels[i, 5, 2] = 'a_pulsating'
    labels[i, 5, 3] = 'a_orbot'
    labels[i, 5, 4] = 'torus'
    labels[i, 5, 5] = 'empty'
    labels[i, 5, 6] = 'empty'
    labels[i, 5, 7] = 'empty'

# add effect
for i in [3,4,5, 8,9,10, 13,14,15, 18,19,20]:
    labels[i, 0, 1] = 'blank'
    labels[i, 0, 2] = 'raindbow'
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
    labels[i, 2, 2] = 'rotate\nblack/ornage'
    labels[i, 2, 3] = 'rotation'

#    labels[i, 3, 0] = 'cut\ncube'
#    labels[i, 3, 1] = 'growing\nsphere'
#    labels[i, 3, 2] = 'outer\nshadow'
#    labels[i, 3, 3] = 'zoom'


#    labels[i, 4, 0] = 'prod\nhue'
#    labels[i, 4, 1] = 'prod\nsaturation'
#    labels[i, 4, 2] = 'fade2blue'
