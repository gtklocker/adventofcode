import fileinput
jumps = [int(x) for x in fileinput.input()]
current = 0
steps = 0
while True:
    prev_jump = jumps[current]
    if prev_jump >= 3:
        jumps[current] -= 1
    else:
        jumps[current] += 1
    current += prev_jump
    steps += 1
    if not (0 <= current < len(jumps)):
        break
print(steps)
