import fileinput
_input = [x.strip() for x in fileinput.input()]

hor, dep = 0, 0
for cmd, X in [(s.split()[0], int(s.split()[1])) for s in _input]:
    if cmd == "forward":
        hor += X
    elif cmd == "up":
        dep -= X
    elif cmd == "down":
        dep += X
    else:
        assert False

print("part 1", hor*dep)

hor, dep, aim = 0, 0, 0
for cmd, X in [(s.split()[0], int(s.split()[1])) for s in _input]:
    if cmd == "forward":
        hor += X
        dep += aim*X
    elif cmd == "up":
        aim -= X
    elif cmd == "down":
        aim += X
    else:
        assert False

print("part 2", hor*dep)
