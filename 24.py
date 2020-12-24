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

for path in paths:
    endedat = proc(path)
    #print(endedat)
    visited[endedat] += 1
print(Counter(visited.values())[1])
