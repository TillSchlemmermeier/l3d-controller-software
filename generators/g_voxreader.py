def gen_world_from_file(filename):
    # generates a world matrix from a file
    temp = np.genfromtxt(filename,delimiter=',')
    # remove "a" at the end
    data = temp[:-1]
    world = world_init(10)
    for i in range(0,len(data)):
        position = (get_position(i))
        if data[i] > 0 :
            world[position[0],position[1],position[2]] = data[i]/255.0
return world

def get_position(i):
    # calculates xyz from position in .vox string

    # add zeros for small numbers
    if i >= 100: position = str(i)
    elif i >= 10: position = '0'+str(i)
    else : position = '00'+str(i)


    if int(position[0])%2 == 0:
        if int(position[1])%2 == 0:
            x = int(position[2])
        else:
            x = 9 - int(position[2])
        y = int(position[1])
    else:
        if int(position[1])%2 == 0:
            x = 9 - int(position[2])
        else:
            x = int(position[2])
        y = 9 - int(position[1])

    z = position[0]

    return x,y,z
