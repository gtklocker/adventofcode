import fileinput
import copy

lines = [list(line.strip()) for line in fileinput.input()]
I = len(lines)
J = len(lines[0])
new_lines = [['']*J for _ in range(I)]

def adjacent(i, j):
    return list((i+di, j+dj) for di in range(-1, 2) for dj in range(-1, 2)
                    if 0 <= i+di < I and 0 <= j+dj < J and not (di == 0 and dj == 0))

def serialize(lines):
    return '\n'.join(''.join(line) for line in lines)

def occupied(lines):
    return sum([line.count('#') for line in lines])

z = 0
while z < 10**10:
    for i in range(I):
        for j in range(J):
            c = lines[i][j]
            if lines[i][j] == 'L' and \
                    all(lines[ii][jj] != '#' for ii, jj in adjacent(i, j)):
                c = '#'
            elif lines[i][j] == '#' and \
                    len([1 for ii, jj in adjacent(i, j) if lines[ii][jj] == '#']) >= 4:
                c = 'L'
            new_lines[i][j] = c
    #print('---')
    if serialize(new_lines) == serialize(lines):
        print(occupied(new_lines))
        break
    #print(serialize(new_lines))
    lines, new_lines = new_lines, lines
    z += 1
