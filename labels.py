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

# add one shots
labels[0, 2, 7] = 'sides'
labels[0, 2, 6] = 'fade'
labels[0, 2, 5] = 'dark'
labels[0, 2, 4] = 'sphere'
labels[0, 3, 7] = 'roll'
labels[0, 3, 6] = 'strobo'
labels[0, 3, 5] = 'cubes'
labels[0, 3, 4] = 'dark sphere'

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
file = open("generators.dat", "r")
generatorFile = file.readlines()

for i in [2, 7, 12, 17]:
    h = 0
    # j is row, k is column
    for j in range(8):
        # first button is close, start at 1 in row 0
        if j == 0:
            for k in range(1, 8):
                # delete first 2 characters
                try:
                    generatorFile[h] = generatorFile[h][2 : : ]
                    if len(generatorFile(h)) > 8:
                        generatorFile[h][:8] + '\n' + generatorFile[h][8:]
                    labels[i,j,k] = generatorFile[h]
                except:
                    pass
                h += 1

        else:

            for k in range(0, 8):
                # delete first 2 characters
                try:
                    generatorFile[h] = generatorFile[h][2 : : ]
                    if len(generatorFile(h)) > 8:
                        generatorFile[h][:8] + '\n' + generatorFile[h][8:]
                    labels[i,j,k] = generatorFile[h]
                except:
                    pass
                h += 1



# add effects
file = open("effects.dat", "r")
effectsFile = file.readlines()

for i in [3,4,5, 8,9,10, 13,14,15, 18,19,20]:
    h = 0
    # j is row, k is column
    for j in range(8):
        # first button is close, start at 1 in row 0
        if j == 0:
            for k in range(1, 8):
                # delete first 2 characters
                try:
                    effectsFile[h] = effectsFile[h][2 : : ]
                    if len(effectsFile(h)) > 8:
                        effectsFile[h][:8] + '\n' + effectsFile[h][8:]
                    labels[i,j,k] = effectsFile[h]
                except:
                    pass
                h += 1

        else:

            for k in range(0, 8):
                # delete first 2 characters
                try:
                    effectsFile[h] = effectsFile[h][2 : : ]
                    if len(effectsFile(h)) > 8:
                        effectsFile[h][:8] + '\n' + effectsFile[h][8:]
                    labels[i,j,k] = effectsFile[h]
                except:
                    pass
                h += 1
