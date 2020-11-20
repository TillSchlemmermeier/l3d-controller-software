file = open("generators.dat", "r")
generatorFile = file.readlines()
generators = []
for generator in generatorFile:
    exec('from generators.' +str(generator).replace('\n','') + ' import *')
    exec('generators.append(' + str(generator).replace('\n','') + ')')

file = open("effects.dat", "r")
effectsFile = file.readlines()
effects = []
for effect in effectsFile:
    exec('from effects.' + str(effect).replace('\n','') + ' import *')
    exec('effects.append(' + str(effect).replace('\n','') + ')')
