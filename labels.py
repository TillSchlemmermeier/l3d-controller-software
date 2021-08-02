import numpy as np


# load presets
preset_labels = []

with open('presets.dat', 'r') as file:
    presets = file.readlines()

for p in presets:
    templabel = p.split()[0]
    if len(templabel) > 8:
        preset_labels.append(templabel[:8]+'\n'+templabel[8:])
    else:
        preset_labels.append(templabel)


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
labels = np.full((26, 8, 8), default)
labels[:,:,:]= ''
# add close labels except for first 'layer'
labels[1:, 0, 0] = 'close'

# add one shots
labels[0, 2, 7] = 'sides'
labels[0, 2, 6] = 'fade'
labels[0, 2, 5] = 'dark'
labels[0, 3, 7] = 'sphere'
labels[0, 3, 6] = 'roll'
labels[0, 3, 5] = 'strobo'
labels[0, 4, 7] = 'cubes'
labels[0, 4, 6] = 'dark sphere'
labels[0, 4, 5] = 'threesixty'

# add global presets
global_preset_labels = []

with open('global_presets.dat', 'r') as file:
    presets = file.readlines()

for p in presets:
    templabel = p.split()[0]
    if len(templabel) > 8:
        global_preset_labels.append(templabel[:8]+'\n'+templabel[8:])
    else:
        global_preset_labels.append(templabel)

for i in [21]:
    counter = 0

    # first row
    for j in range(1, 8):
        if counter < len(global_preset_labels):
            labels[i, 0, j] = global_preset_labels[counter]

        counter += 1

    # second row
    for j in range(0, 8):
        if counter < len(global_preset_labels):
            labels[i, 1, j] = global_preset_labels[counter]

        counter += 1

    #third row
    for j in range(0, 8):
        if counter < len(global_preset_labels):
            labels[i, 2, j] = global_preset_labels[counter]

        counter += 1

    #4th row
    for j in range(0, 8):
        if counter < len(global_preset_labels):
            labels[i, 3, j] = global_preset_labels[counter]

        counter += 1

    #5th row
    for j in range(0, 8):
        if counter < len(global_preset_labels):
            labels[i, 4, j] = global_preset_labels[counter]

        counter += 1

# add presets

for i in [1, 6, 11, 16]:
    counter = 0

    # first row
    for j in range(1, 8):
        if counter < len(preset_labels):
            labels[i, 0, j] = preset_labels[counter]

        counter += 1

    # for next 4 rows
    for row in range(1, 6):
        for column in range(0, 8):
            if counter < len(preset_labels):
                labels[i, row, column] = preset_labels[counter]

            counter += 1


# add generators
file = open("generators.dat", "r")
generatorFile = file.readlines()

# delete first 2 characters
for i in range(len(generatorFile)):
    generatorFile[i] = generatorFile[i][2 : :]

for i in [2, 7, 12, 17]:
    h = 0
    # j is row, k is column
    for j in range(8):
        # first button is close, start at 1 in row 0
        if j == 0:
            for k in range(1, 8):
                # delete first 2 characters
                try:
#                    generatorFile[h] = generatorFile[h][2 : : ]
                    if len(generatorFile[h]) > 8:
                        labels[i,j,k] = generatorFile[h][:8] + '\n' + generatorFile[h][8:]
                    else:
                        labels[i,j,k] = generatorFile[h]
                except:
                    pass
                h += 1

        else:

            for k in range(0, 8):
                # delete first 2 characters
                try:
#                    generatorFile[h] = generatorFile[h][2 : : ]
                    if len(generatorFile[h]) > 8:
                        labels[i,j,k] = generatorFile[h][:8] + '\n' + generatorFile[h][8:]
                    else:
                        labels[i,j,k] = generatorFile[h]
                except:
                    pass
                h += 1



# add effects
file = open("effects.dat", "r")
effectsFile = file.readlines()

for i in range(len(effectsFile)):
    effectsFile[i] = effectsFile[i][2 : :]

# 21 should be global presets

for i in [3,4,5, 8,9,10, 13,14,15, 18,19,20, 22,23,24]:
    h = 0
    # j is row, k is column
    for j in range(8):
        # first button is close, start at 1 in row 0
        if j == 0:
            for k in range(1, 8):
                # delete first 2 characters
                try:
                    # effectsFile[h] = effectsFile[h][2 : : ]
                    if len(effectsFile[h]) > 8:
                        labels[i,j,k] = effectsFile[h][:8] + '\n' + effectsFile[h][8:]
                    else:
                        labels[i,j,k] = effectsFile[h]
                except:
                    pass
                h += 1

        else:

            for k in range(0, 8):
                # delete first 2 characters
                try:
                    # effectsFile[h] = effectsFile[h][2 : : ]
                    if len(effectsFile[h]) > 8:
                        labels[i,j,k] = effectsFile[h][:8] + '\n' + effectsFile[h][8:]
                    else:
                        labels[i,j,k] = effectsFile[h]
                except:
                    pass
                h += 1
