import fileinput

lines = [line.strip().split() for line in fileinput.input()]
instructions = [(v[0], int(v[1])) for v in lines]
acc = 0
i = 0
visited = set()
while True:
    visited.add(i)
    name, val = instructions[i]
    if name == "acc":
        acc += val
        i += 1
    elif name == "jmp":
        i = (i+val) % len(instructions)
    elif name == "nop":
        i += 1
    if i in visited:
        print(acc)
        break
