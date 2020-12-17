import fileinput
from collections import defaultdict

world = defaultdict(lambda: '.')
def neighbouring_coords(x, y, z):
    for dx in range(-1, 1+1):
        for dy in range(-1, 1+1):
            for dz in range(-1, 1+1):
                if all(i == 0 for i in (dx,dy,dz)):
                    continue
                yield (x+dx,y+dy,z+dz)

def neighbors(x, y, z):
    return map(lambda coord: world[coord], neighbouring_coords(x, y, z))

for y, line in enumerate(fileinput.input()):
    for x, char in enumerate(line.strip()):
        if char != '.':
            world[(x,y,0)] = char

def print_world():
    coords_now = world.keys()
    max_dim = [max(coords_now, key=lambda co: co[i])[i] for i in range(3)]
    min_dim = [min(coords_now, key=lambda co: co[i])[i] for i in range(3)]
    for z in range(min_dim[2], max_dim[2]+1):
        print('z=%d' % z)
        for y in range(min_dim[1], max_dim[1]+1):
            print(''.join(world[(x,y,z)] for x in range(min_dim[0], max_dim[0]+1)))
        print()

def step():
    global world
    coords_now = world.keys()
    max_dim = [max(coords_now, key=lambda co: co[i])[i] for i in range(3)]
    min_dim = [min(coords_now, key=lambda co: co[i])[i] for i in range(3)]
    new_world = defaultdict(lambda: '.')
    print(min_dim, max_dim)
    for x in range(min_dim[0]-1, max_dim[0]+2):
        for y in range(min_dim[1]-1, max_dim[1]+2):
            for z in range(min_dim[2]-1, max_dim[2]+2):
                neighboring = list(neighbors(x,y,z))
                if world[(x,y,z)] == '#':
                    if neighboring.count('#') in (2, 3):
                        new_world[(x,y,z)] = '#'
                else:
                    if neighboring.count('#') == 3:
                        new_world[(x,y,z)] = '#'
    world = new_world
for i in range(6):
    step()
print(len(world.values()))
