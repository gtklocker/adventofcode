from collections import defaultdict, deque
import functools
import itertools
import sys
import math
import numpy as np

def parse_tile(string):
    before, after = string.split(':')
    tile_id = int(before.split()[-1])
    actual_tile = np.array(list(map(list, after.split())))
    return (tile_id, actual_tile)

tile_strs = sys.stdin.read().strip().split('\n\n')
tiles = {}

for string in tile_strs:
    tile_id, actual_tile = parse_tile(string)
    tiles[tile_id] = actual_tile

def borders(tile):
    return set([
        ''.join(tile[0,:]), ''.join(tile[0,:][::-1]), # up
        ''.join(tile[:,0]), ''.join(tile[:,0][::-1]), # left
        ''.join(tile[-1,:]), ''.join(tile[-1,:][::-1]), # down
        ''.join(tile[:,-1]), ''.join(tile[:,-1][::-1]), # right
    ])

neighbors = defaultdict(lambda: [])
common = {}
for t1, t2 in itertools.combinations(tiles, 2):
    intersection = borders(tiles[t1]) & borders(tiles[t2])
    if len(intersection) > 0:
        common[(t1,t2)] = common[(t2,t1)] = intersection
        neighbors[t1].append(t2)
        neighbors[t2].append(t1)
corners = [i for i in neighbors if len(neighbors[i]) == 2]
n = math.isqrt(len(tiles))
grid = defaultdict(lambda: 0)
rot90s = defaultdict(lambda: 0)
lrflips = defaultdict(lambda: False)
udflips = defaultdict(lambda: False)

def sides(tile_id, rots, lrs, uds):
    tile = transformed_tile(tiles[tile_id], rots, lrs, uds)
    return {
        1j: ''.join(tile[-1,:]), # down
        -1j: ''.join(tile[0,:]), # up
        1: ''.join(tile[:,-1]), # right
        -1: ''.join(tile[:,0]), # left
    }

def transformed_tile(tile, rots, lrs, uds):
    tile = np.rot90(tile, rots)
    if lrs:
        tile = np.fliplr(tile)
    if uds:
        tile = np.flipud(tile)
    return tile

def transformed_placed_tile(tile_loc):
    return transformed_tile(tiles[grid[tile_loc]], rot90s[tile_loc], lrflips[tile_loc], udflips[tile_loc])

def placed_sides(tile_loc):
    return sides(grid[tile_loc], rot90s[tile_loc], lrflips[tile_loc], udflips[tile_loc])

grid[0] = corners[0]
frontier = deque([(0, -1)]) # tuples in the form (current, parent)
#import sys
#print(placed_sides(0))
#sys.exit()
#rot90s[0] = 1
#lrflips[0] = 1
placed = set([grid[0]])
while frontier:
    current, parent = frontier[0]
    if current not in grid:
        print(current)
        parent_id = grid[parent]
        for candidate_id in neighbors[parent_id]:
            if candidate_id in placed:
                continue
            print('trying neighbor', candidate_id, 'with parent', parent_id)
            delta = current-parent
            common_sides = common[(candidate_id, parent_id)]
            print('common sides were', common_sides)
            parent_side = placed_sides(parent)[delta]
            print('parent side with delta', delta, 'is', parent_side)
            if parent_side not in common_sides:
                continue

            cemented = False
            for r90, flip in itertools.product(range(4), range(3)):
                # flip = [0 no flip, 1 flip lr, 2 flip ud]
                current_side = sides(candidate_id, r90, flip == 1, flip == 2)[-delta]
                if current_side == parent_side:
                    print('side matched', current_side, r90, flip)
                    rot90s[current] = r90
                    lrflips[current] = flip == 1
                    udflips[current] = flip == 2
                    grid[current] = candidate_id
                    placed.add(candidate_id)
                    cemented = True
                    break
            if cemented:
                print('matched with neighbor', candidate_id)
                break
    if parent == 0 and current not in grid:
        r90, lr, ud = (rot90s[0], lrflips[0], udflips[0])
        if lr == 1:
            lr = 0
            ud = 1
        elif ud == 1:
            r90 += 1
            lr = 0
            ud = 0
        else:
            lr = 1
        rot90s[0], lrflips[0], udflips[0] = r90, lr, ud
        print('trying another flip for anchor')
        frontier.appendleft((current, parent))
    else:
        frontier.popleft()

    for delta in (-1j, 1j, 1, -1):
        new = current+delta
        if 0 <= new.real < n and 0 <= new.imag < n and new not in grid:
            frontier.append((new, current))
pretty_grid = np.zeros((n,n))
for a, b in grid.items():
    pretty_grid[int(a.imag),int(a.real)] = b
print(pretty_grid)
some_tile = next(iter(tiles.values()))
m = some_tile.shape[0]-2
full_grid = np.empty((n*m, n*m), dtype=str)
print(n, m)
for tile_loc in grid:
    x, y = int(tile_loc.real), int(tile_loc.imag)
    full_grid[y*m:(y+1)*m,x*m:(x+1)*m] = \
            transformed_placed_tile(tile_loc)[1:-1,1:-1]
#print(full_grid)
monster = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """
monster_positions = []
for y, line in enumerate(monster.split('\n')):
    for x, c in enumerate(line):
        if c == '#':
            monster_positions.append(x+y*1j)
for r90, flip in itertools.product(range(4), range(3)):
    monsters = 0
    transformed_grid = transformed_tile(full_grid, r90, flip == 1, flip == 2)
    all_monster_hashes = set()
    for row in range(n*m):
        for col in range(n*m):
            monster_hashes = set()
            matches = True
            for p in monster_positions:
                mp = row*1j+col+p
                mx, my = int(mp.real), int(mp.imag)
                if my >= n*m or mx >= n*m or transformed_grid[my,mx] != '#':
                    matches = False
                    break
                elif transformed_grid[my,mx] == '#':
                    monster_hashes.add((my, mx))
            if matches:
                all_monster_hashes |= monster_hashes
                monsters += 1
    if monsters > 0:
        ans = 0
        for row in range(n*m):
            for col in range(n*m):
                if transformed_grid[row,col] == '#' and (row,col) not in all_monster_hashes:
                    ans += 1
        print('rot', r90, 'flip', flip)
        print('matched monsters', monsters)
        print('answer', ans)
        break
#print('monsters found', monsters)
#print(transformed_grid)
