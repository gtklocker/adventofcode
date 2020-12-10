import fileinput

lines = [line.strip().split() for line in fileinput.input()]
instructions = [(v[0], int(v[1])) for v in lines]

for c in range(len(instructions)):
    if instructions[c][0] not in ("nop", "jmp"):
        continue
    acc = 0
    i = 0
    visited = set()
    infloop = False
    while i < len(instructions):
        visited.add(i)
        name, val = instructions[i]
        if name == "acc":
            acc += val
            i += 1
        elif (name == "jmp" and i != c) or (name == "nop" and i == c):
            i += val
        elif (name == "nop" and i != c) or (name == "jmp" and i == c):
            i += 1
        if i in visited:
            infloop = True
            break
    if not infloop:
        print(acc)
