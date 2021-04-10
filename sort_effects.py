from copy import deepcopy
import sys
import numpy as np

def swap_eff(effects, effect1, effect2):

    ind1 = np.where(np.array(effects) == effect1+'\n')[0][0]
    ind2 = np.where(np.array(effects) == effect2+'\n')[0][0]

    temp = deepcopy(effects)
    temp[ind1] = effect2+'\n'
    temp[ind2] = effect1+'\n'

    return temp

def append_eff(effects, new_effect):
    temp = deepcopy(effects)
    temp.append(new_effect+'\n')
    return temp


def insert_eff(effects, new_effect, pos):
    temp = deepcopy(effects)
    temp.insert(pos, new_effect+'\n')
    return temp


def remove_eff(effects, remove_effect):
    effect_used = False
    temp = deepcopy(effects)
    index = temp.index(remove_effect + '\n')

    with open('presets.dat', 'r') as file:
        presets = file.readlines()

    list_presets = []
    for p in presets:
        list_presets.append(p.strip('\n').split())

    for preset in list_presets:
        # loop over effects
        for j in range(2, 5):
            if int(float(preset[j])) == index:
                effect_used = True
                print("effect used in preset " + preset[0] + ". Edit or remove preset first")


    with open('global_presets.dat', 'r') as file:
        presets = file.readlines()

    list_presets = []
    for p in presets:
        list_presets.append(p.strip('\n').split())

    for preset in list_presets:
        # loop over channels
        for i in range(4):
            # loop over effects
            for j in range(2, 5):
                if int(float(preset[5*i+j])) == index:
                    effect_used = True
                    print("effect used in global preset " + preset[0] + ". Edit or remove global preset first")

        # loop over global effects
        for i in range(3):
            if int(float(preset[140+i])) == index:
                effect_used = True
                print("effect used in global preset " + preset[0] + " as global effect. Edit or remove global preset first")


    if not effect_used:
        temp.remove(remove_effect + '\n')
        print("effect " + remove_effect + " removed")

    return temp


def get_dictionary(old_effs, new_effs):

    swap_dict = {}
    old_effs = np.array(old_effs)
    new_effs = np.array(new_effs)

    for i in range(len(old_effs)):
        try:
            ind = int(np.where(old_effs[i] == new_effs)[0][0])
            swap_dict[i] = ind
        except:
            print("making dictionary, effect " + str(i) + " now missing")

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
        for j in range(2, 5):
            ind = int(float(preset[j]))
            preset[j] = str(swap_dict[ind])

    print('trying to save presets...')
    # saving modified presets
    with open('presets.dat', 'w') as file:
        for preset in list_presets:
            file.write(' '.join(preset) + '\n')
    print("presets successfully saved")

def update_global_presets(swap_dict):
    # loading and parsing presets
    with open('global_presets.dat', 'r') as file:
        presets = file.readlines()

    list_presets = []
    for p in presets:
        list_presets.append(p.strip('\n').split())

    # change number
    for preset in list_presets:
        # loop over channels
        for i in range(4):
            # loop over effects
            for j in range(2, 5):
                ind = int(float(preset[5*i+j]))
                preset[5*i+j] = str(swap_dict[ind])

        # loop over global effects
        for i in range(3):
            ind = int(float(preset[140+i]))
            preset[140+i] = str(swap_dict[ind])

    print('trying to save global presets...')
    # saving modified presets
    with open('global_presets.dat', 'w') as file:
        for preset in list_presets:
            file.write(' '.join(preset) + '\n')
    print("global presets successfully saved")


if __name__ == "__main__":
    print(sys.argv)


    with open('effects.dat', 'r') as file:
        effects = file.readlines()

    if sys.argv[1] == 'a':
        new_effects = append_eff(effects, sys.argv[2])
    elif sys.argv[1] == 'i':
        new_effects = insert_eff(effects, sys.argv[2], int(sys.argv[3]))
    elif sys.argv[1] == 's':
        new_effects = swap_eff(effects, sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'r':
        new_effects = remove_eff(effects, sys.argv[2])

    if effects != new_effects:
        swap_dict = get_dictionary(effects, new_effects)
        update_presets(swap_dict)
        update_global_presets(swap_dict)

        with open('effects.dat', 'w') as file:
            for line in new_effects:
                file.write(line)
        print("effects.dat updated")

    else:
        print("no changes saved")

'''
    except:
        print('ERROR!' )
        print('usage: python3.8 sort_effects.py <a/i/s> <new_effect/new_effect/effect 1> <NaN/pos/effect 2>')
'''
