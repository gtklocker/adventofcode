import fileinput
from collections import defaultdict
import itertools

world = set()
n_space = 4
def neighbouring_coords(coord):
    for delta in itertools.product(*[range(-1, 1+1) for _ in range(n_space)]):
        if all(i == 0 for i in delta):
            continue
        yield tuple([coord[i]+delta[i] for i in range(n_space)])

def active_neighbors(coord):
    return sum(1 for co in neighbouring_coords(coord) if co in world)

next_step = set()
for y, line in enumerate(fileinput.input()):
    for x, char in enumerate(line.strip()):
        if char != '.':
            coord = tuple([x,y] + [0]*(n_space-2))
            world.add(coord)
            next_step |= set(neighbouring_coords(coord))

def step():
    global world, next_step
    max_dim = [max(world, key=lambda co: co[i])[i] for i in range(n_space)]
    min_dim = [min(world, key=lambda co: co[i])[i] for i in range(n_space)]
    new_world = set()
    new_next_step = set()
    for spot in next_step:
        act = active_neighbors(spot)
        active = False
        if spot in world and act in (2, 3):
            active = True
        elif act == 3:
            active = True
        if active:
            new_world.add(spot)
            new_next_step |= set(neighbouring_coords(spot))
    world = new_world
    next_step = new_next_step

for i in range(6):
    step()
print(len(world))
