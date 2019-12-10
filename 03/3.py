def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def apply_move(move, pos):
    direction, length = move

    if direction == 'U':
        new_pos = pos[0], pos[1] + length
    if direction == 'D':
        new_pos = pos[0], pos[1] - length
    if direction == 'L':
        new_pos = pos[0] - length, pos[1]
    if direction == 'R':
        new_pos = pos[0] + length, pos[1]
    return new_pos

def parse_move(s):
    return s[0], int(s[1:])

def in_segment(seg, pt):
    x_eq = seg[0][0] == seg[1][0] and seg[0][0] == pt[0] and seg[0][1] <= pt[1] <= seg[1][1]
    y_eq = seg[0][1] == seg[1][1] and seg[0][1] == pt[1] and seg[0][0] <= pt[0] <= seg[1][0]
    return x_eq or y_eq

def points_between(a, b):
    dim = 1 if a[0] == b[0] else 0
    incr = 1 if a[dim] <= b[dim] else -1
    for i in range(a[dim], b[dim]+incr, incr):
        if dim == 1: yield a[0], i
        else: yield i, a[1]

def trace(moves):
    pos = (0, 0)
    ret = set()
    for move in moves:
        prev_pos = pos
        pos = apply_move(move, pos)
        for pt in points_between(prev_pos, pos):
            ret.add(pt)
    return ret

def tail(xs):
    next(xs)
    return xs

def trace_with_steps(moves):
    pos = (0, 0)
    steps = 1
    step_by_pt = {}
    for move in moves:
        prev_pos = pos
        pos = apply_move(move, pos)
        for pt in tail(points_between(prev_pos, pos)):
            if pt not in step_by_pt:
                step_by_pt[pt] = steps
            steps += 1
    return step_by_pt

def solve_one(first_moves, second_moves):
    first_trace = trace(first_moves)
    second_trace = trace(second_moves)
    return min(dist((0, 0), pt) for pt in (first_trace & second_trace) - {(0, 0)})

def solve_two(first_moves, second_moves):
    first_trace = trace_with_steps(first_moves)
    second_trace = trace_with_steps(second_moves)
    common_pts = first_trace.keys() & second_trace.keys()
    return min(first_trace[pt] + second_trace[pt] for pt in common_pts)

with open("input.txt", "r") as f:
    first_moves, second_moves = [list(map(parse_move, line.strip().split(','))) for line in f]
    print(solve_one(first_moves, second_moves))
    print(solve_two(first_moves, second_moves))