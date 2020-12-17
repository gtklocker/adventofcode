import fileinput
from collections import defaultdict

world = defaultdict(lambda: '.')
def neighbouring_coords(x, y, z, w):
    for dx in range(-1, 1+1):
        for dy in range(-1, 1+1):
            for dz in range(-1, 1+1):
                for dw in range(-1, 1+1):
                    if all(i == 0 for i in (dx,dy,dz,dw)):
                        continue
                    yield (x+dx,y+dy,z+dz,w+dw)

def neighbors(x, y, z, w):
    return map(lambda coord: world[coord], neighbouring_coords(x, y, z, w))

for y, line in enumerate(fileinput.input()):
    for x, char in enumerate(line.strip()):
        if char != '.':
            world[(x,y,0,0)] = char

def print_world():
    coords_now = world.keys()
    max_dim = [max(coords_now, key=lambda co: co[i])[i] for i in range(4)]
    min_dim = [min(coords_now, key=lambda co: co[i])[i] for i in range(4)]
    for z in range(min_dim[2], max_dim[2]+1):
        print('z=%d' % z)
        for y in range(min_dim[1], max_dim[1]+1):
            print(''.join(world[(x,y,z)] for x in range(min_dim[0], max_dim[0]+1)))
        print()

def step():
    global world
    coords_now = world.keys()
    max_dim = [max(coords_now, key=lambda co: co[i])[i] for i in range(4)]
    min_dim = [min(coords_now, key=lambda co: co[i])[i] for i in range(4)]
    new_world = defaultdict(lambda: '.')
    print(min_dim, max_dim)
    for x in range(min_dim[0]-1, max_dim[0]+2):
        for y in range(min_dim[1]-1, max_dim[1]+2):
            for z in range(min_dim[2]-1, max_dim[2]+2):
                for w in range(min_dim[3]-1, max_dim[3]+2):
                    spot = (x,y,z,w)
                    neighboring = list(neighbors(*spot))
                    if world[spot] == '#':
                        if neighboring.count('#') in (2, 3):
                            new_world[spot] = '#'
                    else:
                        if neighboring.count('#') == 3:
                            new_world[spot] = '#'
    world = new_world
for i in range(6):
    step()
print(len(world.values()))
