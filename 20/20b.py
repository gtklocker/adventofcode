from collections import defaultdict, deque, namedtuple

maze = defaultdict(lambda: ' ')
positions_by_portal = defaultdict(lambda: set())
directions = [-1, 1, 1j, -1j]
entrance, exit = None, None
w, h = 0, 0

Portal = namedtuple('Portal', ['name', 'outward'])
Place = namedtuple('Place', ['pos', 'level'])

def adj_portal(pos):
    if maze[pos] != '.':
        return None
    down = [1j, 2j, 3j]
    up = [-2j, -1j, -3j]
    left = [-2, -1, -3]
    right = [1, 2, 3]

    for a, b, c in (up, right, down, left):
        candidate = maze[pos+a] + maze[pos+b]
        if candidate.isalnum():
            outward = pos+c not in maze
            return Portal(candidate, outward)

def teleport_position(place):
    portal = adj_portal(place.pos)
    if portal is None or portal.name in {'AA', 'ZZ'}:
        return None
    new_level = place.level-1 if portal.outward else place.level+1
    if new_level < 0:
        return None
    return Place(pos=next(iter(positions_by_portal[portal.name] - {place.pos})), level=new_level)


def moves_from(place):
    teleport_move = teleport_position(place)
    normal_moves = [Place(place.pos+delta, place.level) for delta in directions if maze[place.pos+delta] == '.']
    if teleport_move is None:
        return normal_moves
    return normal_moves + [teleport_move]

def print_maze(maze):
    xs = [int(k.real) for k in maze.keys()]
    ys = [int(k.imag) for k in maze.keys()]
    lines = []
    for y in range(min(ys), max(ys)+1):
        line = []
        for x in range(min(xs), max(xs)+1):
            pt = x+y*1j
            line.append(maze[pt] if pt in maze else ' ')
        lines.append(''.join(line))
    print('\n'.join(lines))

with open('input.txt') as f:
    for y, row in enumerate(f.readlines()):
        row = row.rstrip()
        h = y+1
        w = max(w, len(row))
        for x, c in enumerate(row):
            maze[x+y*1j] = c

for y in range(h):
    for x in range(w):
        pos = x + y*1j
        portal = adj_portal(pos)
        if portal is not None:
            if portal.name == 'AA':
                entrance = Place(pos, 0)
            if portal.name == 'ZZ':
                exit = Place(pos, 0)
            positions_by_portal[portal.name].add(pos)
            print('got portal', portal, 'in position', pos)

q = deque([(entrance, 0)])
visited = set()
while len(q) > 0:
    place, dist = q.popleft()
    if place == exit:
        print(pos, dist, exit)
        break
    for nplace in moves_from(place):
        new_state = (nplace, dist+1)
        if nplace not in visited:
            visited.add(nplace)
            q.append(new_state)
