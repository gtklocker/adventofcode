from collections import Counter
import fileinput

_input = [x.strip() for x in fileinput.input()]

def norm(v):
    div = abs(v[0]) if v[0] != 0 else abs(v[1])
    return (v[0]//div,v[1]//div)

paths = []
for line in _input:
    s = [tuple(int(x) for x in s.split(',')) for s in line.split(" -> ")]
    paths.append(s)
grid = Counter()
for path in paths:
    _from, _to = path[0], path[1]
    delta = norm((_to[0]-_from[0], _to[1]-_from[1]))
    grid[_from] += 1
    while _from != _to:
        _from = (_from[0]+delta[0], _from[1]+delta[1])
        grid[_from] += 1
print(len([x for x in grid.values() if x > 1]))
