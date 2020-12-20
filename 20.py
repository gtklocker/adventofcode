from collections import defaultdict
import itertools
import sys
import math

def parse_tile(string):
    before, after = string.split(':')
    tile_id = int(before.split()[-1])
    actual_tile = after.split()
    return (tile_id, actual_tile)
tile_strs = sys.stdin.read().strip().split('\n\n')
tiles = {}
for string in tile_strs:
    tile_id, actual_tile = parse_tile(string)
    tiles[tile_id] = actual_tile

def borders(tile):
    return set([
        tile[0], tile[-1], tile[0][::-1], tile[-1][::-1], \
        ''.join(tile[i][0] for i in range(len(tile))),
        ''.join(tile[i][-1] for i in range(len(tile))),
        ''.join(tile[i][0] for i in range(len(tile)))[::-1],
        ''.join(tile[i][-1] for i in range(len(tile)))[::-1],
    ])

intersects = defaultdict(lambda:0)
for t1, t2 in itertools.combinations(tiles, 2):
    intersection = borders(tiles[t1]) & borders(tiles[t2])
    if len(intersection) > 0:
        intersects[t1] += 1
        intersects[t2] += 1
print(math.prod([i for i in intersects if intersects[i] == 2]))
