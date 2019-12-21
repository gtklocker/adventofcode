from collections import defaultdict, deque

maze = defaultdict(lambda: ' ')
positions_by_portal = defaultdict(lambda: set())
directions = [-1, 1, 1j, -1j]
entrance, exit = None, None
w, h = 0, 0

def adj_portal(pos):
    if maze[pos] != '.':
        return None
    down = ''.join([maze[pos+1j], maze[pos+2j]])
    up = ''.join([maze[pos-2j], maze[pos-1j]])
    left = ''.join([maze[pos-2], maze[pos-1]])
    right = ''.join([maze[pos+1], maze[pos+2]])

    adj_portals = [s for s in [up, right, down, left] if s.isalnum()]
    if len(adj_portals) > 0:
        assert len(adj_portals) == 1
        return adj_portals[0]

def teleport_position(pos):
    portal = adj_portal(pos)
    if portal is None or portal in {'AA', 'ZZ'}:
        return None
    return next(iter(positions_by_portal[portal] - {pos}))

def moves_from(pos):
    teleport_move = teleport_position(pos)
    normal_moves = [pos+delta for delta in directions if maze[pos+delta] == '.']
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
            if portal == 'AA':
                entrance = pos
            if portal == 'ZZ':
                exit = pos
            positions_by_portal[portal].add(pos)
            print('got portal', portal, 'in position', pos)

q = deque([(entrance, 0)])
visited = set()
while len(q) > 0:
    pos, dist = q.popleft()
    if pos == exit:
        print(pos, dist, exit)
        break
    for npos in moves_from(pos):
        new_state = (npos, dist+1)
        if new_state not in visited:
            visited.add(new_state)
            q.append(new_state)
