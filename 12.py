import math
import fileinput

def parse_line(line):
    line = line.strip()
    return (line[0], int(line[1:]))
lines = [parse_line(line) for line in fileinput.input()]
direction = 1
pos = 0

def rot(direction, angle, lr):
    rotv = -1j if lr == 'R' else 1j
    return direction * rotv**(angle//90)

for (d, n) in lines:
    if d == 'E':
        pos += n
    elif d == 'W':
        pos -= n
    elif d == 'N':
        pos += n*1j
    elif d == 'S':
        pos -= n*1j
    elif d == 'F':
        pos += n*direction
    elif d in ('L', 'R'):
        direction = rot(direction, n, d)

print(abs(pos.real)+abs(pos.imag))
