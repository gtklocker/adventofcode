import fileinput
from collections import Counter

paths = list(l.strip() for l in fileinput.input())

DIRECTIONS = {
    "nw": -1j,
    "ne": 1-1j,
    "se": 1+1j,
    "sw": 1j,
    "w": -1,
    "e": 1
}
visited = Counter()
def proc(path):
    pos = 0
    while path:
        for d in DIRECTIONS:
            if path[:len(d)] == d:
                ourdir = d
                path = path[len(d):]
                break
        actdir = DIRECTIONS[ourdir]
        if len(ourdir) == 2 and pos.imag % 2 == 1:
            actdir -= 1
        pos += actdir
    return pos

BLACK = 1
WHITE = 2
def neighbors(tile):
    for d in DIRECTIONS:
        actdir = DIRECTIONS[d]
        if len(d) == 2 and tile.imag % 2 == 1:
            actdir -= 1
        yield tile+actdir

def black_neighbors(tile):
    return len([pos for pos in neighbors(tile) if pos in visited and visited[pos] == BLACK])

def step():
    global visited
    new_visited = {}
    to_check = set.union(*[set(neighbors(tile)) for tile in visited if visited[tile] == BLACK])
    for tile in to_check:
        neigh = black_neighbors(tile)
        if tile in visited and visited[tile] == BLACK and (neigh == 0 or neigh > 2):
            new_visited[tile] = WHITE
        elif (tile not in visited or visited[tile] == WHITE) and neigh == 2:
            new_visited[tile] = BLACK
        elif tile in visited:
            new_visited[tile] = visited[tile]
    visited = new_visited

for path in paths:
    endedat = proc(path)
    visited[endedat] += 1
print(Counter(visited.values())[BLACK])
for i in range(100):
    step()
print(Counter(visited.values())[BLACK])
