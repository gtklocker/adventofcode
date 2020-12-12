import math
import fileinput

def parse_line(line):
    line = line.strip()
    return (line[0], int(line[1:]))
lines = [parse_line(line) for line in fileinput.input()]
pos = 0
waypoint = 10+1j

def rot(angle, lr):
    rotv = -1j if lr == 'R' else 1j
    return pos + ((waypoint-pos) * rotv**(angle//90))

for (d, n) in lines:
    if d == 'E':
        waypoint += n
    elif d == 'W':
        waypoint -= n
    elif d == 'N':
        waypoint += n*1j
    elif d == 'S':
        waypoint -= n*1j
    elif d == 'F':
        move = n*(waypoint-pos)
        pos += move
        waypoint += move
    elif d in ('L', 'R'):
        waypoint = rot(n, d)

print(abs(pos.real)+abs(pos.imag))
