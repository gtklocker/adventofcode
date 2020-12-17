import fileinput
from collections import defaultdict
import itertools

world = defaultdict(lambda: '.')
n_space = 3
def neighbouring_coords(coord):
    for delta in itertools.product(*[range(-1, 1+1) for _ in range(n_space)]):
        if all(i == 0 for i in delta):
            continue
        yield tuple([coord[i]+delta[i] for i in range(n_space)])

def neighbors(coord):
    return map(lambda coord: world[coord], neighbouring_coords(coord))

for y, line in enumerate(fileinput.input()):
    for x, char in enumerate(line.strip()):
        if char != '.':
            coord = tuple([x,y] + [0]*(n_space-2))
            world[coord] = char

def step():
    global world
    coords_now = world.keys()
    max_dim = [max(coords_now, key=lambda co: co[i])[i] for i in range(n_space)]
    min_dim = [min(coords_now, key=lambda co: co[i])[i] for i in range(n_space)]
    new_world = defaultdict(lambda: '.')
    for spot in itertools.product(
            *[range(min_dim[i]-1, max_dim[i]+2) for i in range(n_space)]
    ):
        neighboring = list(neighbors(spot))
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
