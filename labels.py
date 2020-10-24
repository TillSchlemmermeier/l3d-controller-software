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

    # first row
    for j in range(1, 8):
        if counter < len(preset_labels):
            print(j, counter)
            labels[i, 0, j] = preset_labels[counter]

        counter += 1

    # second row
    for j in range(0, 8):
        if counter < len(preset_labels):
            print(j, counter)
            labels[i, 1, j] = preset_labels[counter]

        counter += 1

    #third grow
    for j in range(0, 8):
        if counter < len(preset_labels):
            print (j, counter)
            labels[i, 2, j] = preset_labels[counter]

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
    labels[i, 1, 2] = 'oblique\nplaneXYZ'
    labels[i, 1, 3] = 'growing\nface'
    labels[i, 1, 4] = 'snake'
    labels[i, 1, 5] = 'sides'
    labels[i, 1, 6] = 'sound_lines'
    labels[i, 1, 7] = 'shooting\nstar'

    labels[i, 2, 0] = 'rotating\nplane'
    labels[i, 2, 1] = 'random\nlines'
    labels[i, 2, 2] = 'random\ncross'
    labels[i, 2, 3] = 'rain'
    labels[i, 2, 4] = 'orbiter'
    labels[i, 2, 5] = 'growing_sphere_rand'
    labels[i, 2, 6] = 'text'
    labels[i, 2, 7] = 'pyramid'

    labels[i, 3, 0] = 'pyramid\n(upside)'
    labels[i, 3, 1] = 'in and\nout'
    labels[i, 3, 2] = 'growing\ncorner'
    labels[i, 3, 3] = 'falling '
    labels[i, 3, 4] = 'drop'
    labels[i, 3, 5] = 'oblique\nplane'
    labels[i, 3, 6] = 'cut'
    labels[i, 3, 7] = 'multicube'

    labels[i, 4, 0] = 'cube edges'
    labels[i, 4, 1] = 'corner'
    labels[i, 4, 2] = 'corner\ngrow'
    labels[i, 4, 3] = 'columns'
    labels[i, 4, 4] = 'circles'
    labels[i, 4, 5] = 'grow'
    labels[i, 4, 6] = 'sound\nsphere'
    labels[i, 4, 7] = 'swell'

    labels[i, 5, 0] = 'smiley'
    labels[i, 5, 1] = 'a_multi\ncube_edges'
    labels[i, 5, 2] = 'centralglow'
    labels[i, 5, 3] = 'a_orbot'
    labels[i, 5, 4] = 'torus'
    labels[i, 5, 5] = 'pong'
    labels[i, 5, 6] = 'edgelines'
    labels[i, 5, 7] = 'soundcube'

    labels[i, 6, 0] = 'sinus'
    labels[i, 6, 1] = 'sound\nellipsoid'

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
    labels[i, 3, 2] = 'randomizer'
#    labels[i, 3, 3] = 'rainbownew'
#    labels[i, 3, 2] = 'outer\nshadow'
#    labels[i, 3, 3] = 'zoom'


#    labels[i, 4, 0] = 'prod\nhue'
#    labels[i, 4, 1] = 'prod\nsaturation'
#    labels[i, 4, 2] = 'fade2blue'
