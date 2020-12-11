import fileinput
import copy

lines = [list(line.strip()) for line in fileinput.input()]
I = len(lines)
J = len(lines[0])
new_lines = [['']*J for _ in range(I)]

def adjacent(i, j, lst):
    for di in range(-1, 2):
        for dj in range(-1, 2):
            if di == 0 and dj == 0:
                continue
            ddi, ddj = di, dj
            found = False
            while 0 <= i+ddi < I and 0 <= j+ddj < J:
                if lst[i+ddi][j+ddj] != '.':
                    found = True
                    yield lst[i+ddi][j+ddj]
                    break
                ddi += di
                ddj += dj
            if not found:
                yield '.'

def serialize(lines):
    return '\n'.join(''.join(line) for line in lines)

def occupied(lines):
    return sum([line.count('#') for line in lines])

while True:
    changed = False
    for i in range(I):
        for j in range(J):
            c = lines[i][j]
            adj = list(adjacent(i, j, lines))
            if lines[i][j] == 'L' and all(a != '#' for a in adj):
                changed = True
                c = '#'
            elif lines[i][j] == '#' and adj.count('#') >= 5:
                changed = True
                c = 'L'
            new_lines[i][j] = c
    if not changed:
        print(occupied(new_lines))
        break
    lines, new_lines = new_lines, lines
