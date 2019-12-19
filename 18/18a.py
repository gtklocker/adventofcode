canvas = {}
reverse_canvas = {}
all_keys = set()

def is_door(pos):
    return canvas[pos].isupper() and canvas[pos].isalnum()

def is_key(pos):
    return canvas[pos].islower() and canvas[pos].isalnum()

with open("input.txt") as f:
    for row, line in enumerate(f.readlines()):
        line = line.strip()
        h = row+1
        for col, c in enumerate(line):
            w = col+1
            pos = col + row*1j
            if c == '@':
                entrance = pos
            canvas[pos] = c
            if is_key(pos):
                all_keys.add(c)
            if c == '@' or is_key(pos) or is_door(pos):
                reverse_canvas[c] = pos

def print_canvas():
    for y in range(h):
        for x in range(w):
            print(canvas[x + y*1j], end='')
        print()

from collections import deque, namedtuple

State = namedtuple('State', ['pos', 'dist', 'keys'])
def solve(starting_pos):
    q = deque([State(pos=starting_pos, dist=0, keys=frozenset())])
    visited = set([(starting_pos, frozenset())])
    z = {}
    while len(q) > 0:
        state = q.popleft()
        if len(state.keys) > len(z):
            print(state.keys)
            z = state.keys
        if len(state.keys) == len(all_keys):
            return state
        
        for move in (1, -1, 1j, -1j):
            new_pos = state.pos + move
            if new_pos not in canvas or canvas[new_pos] == '#':
                continue
            if is_door(new_pos) and canvas[new_pos].lower() not in state.keys:
                continue

            new_keys = state.keys if not is_key(new_pos) else state.keys | frozenset(canvas[new_pos])
            new_state = State(pos=new_pos, dist=state.dist+1, keys=new_keys)
            if (new_pos, new_keys) not in visited:
                q.append(new_state)
                visited.add((new_pos, new_keys))

print(solve(entrance))
