from copy import deepcopy
import sys
import numpy as np

def swap_gen(generators, generator1, generator2):

    ind1 = np.where(np.array(generators) == generator1+'\n')[0][0]
    ind2 = np.where(np.array(generators) == generator2+'\n')[0][0]

    temp = deepcopy(generators)
    temp[ind1] = generator2+'\n'
    temp[ind2] = generator1+'\n'

    return temp

def append_gen(generators, new_generator):
    temp = deepcopy(generators)
    temp.append(new_generator+'\n')
    return temp


def insert_gen(generators, new_generator, pos):
    temp = deepcopy(generators)
    temp.insert(pos, new_generator+'\n')
    return temp

def get_dictionary(old_gens, new_gens):

    swap_dict = {}
    old_gens = np.array(old_gens)
    new_gens = np.array(new_gens)

    for i in range(len(old_gens)):
        ind = int(np.where(old_gens[i] == new_gens)[0][0])
        swap_dict[i] = ind

    return swap_dict

def update_presets(swap_dict):
    # loading and parsing presets
    with open('presets.dat', 'r') as file:
        presets = file.readlines()

    list_presets = []
    for p in presets:
        list_presets.append(p.strip('\n').split())

    # change number
    for preset in list_presets:
        ind = int(float(preset[1]))
        preset[1] = str(swap_dict[ind])

    print('trying to save file...')
    # saving modified presets
    with open('presets.dat', 'w') as file:
        for preset in list_presets:
            file.write(' '.join(preset) + '\n')


def update_global_presets(swap_dict):
    # loading and parsing presets
    with open('global_presets.dat', 'r') as file:
        presets = file.readlines()

    list_presets = []
    for p in presets:
        list_presets.append(p.strip('\n').split())

    # change number
    for preset in list_presets:
        ind = int(float(preset[1]))
        preset[1] = str(swap_dict[ind])
        ind = int(float(preset[6]))
        preset[6] = str(swap_dict[ind])
        ind = int(float(preset[11]))
        preset[11] = str(swap_dict[ind])
        ind = int(float(preset[16]))
        preset[16] = str(swap_dict[ind])

    # saving modified presets
    with open('global_presets.dat', 'w') as file:
        for preset in list_presets:
            file.write(' '.join(preset) + '\n')


if __name__ == "__main__":
    print(sys.argv)

    try:
        with open('generators.dat', 'r') as file:
            generators = file.readlines()

        if sys.argv[1] == 'a':
            new_generators = append_gen(generators, sys.argv[2])
        elif sys.argv[1] == 'i':
            new_generators = insert_gen(generators, sys.argv[2], int(sys.argv[3]))
        elif sys.argv[1] == 's':
            new_generators = swap_gen(generators, sys.argv[2], sys.argv[3])


        swap_dict = get_dictionary(generators, new_generators)
        update_presets(swap_dict)
        update_global_presets(swap_dict)

        with open('generators.dat', 'w') as file:
            for line in new_generators:
                file.write(line)
    except:
        print('ERROR!' )
        print('usage: python3.8 sort_generators.py <a/i/s> <new_generator/new_generator/generator 1> <NaN/pos/generator 2>')
