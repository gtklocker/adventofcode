from collections import defaultdict, deque
numbers = [1,17,0,10,18,11,6]
positions = defaultdict(deque)
for i, n in enumerate(numbers):
    positions[n].append(i)

# Didn't need to do anything special for part 2. 3e7 means we'll just take 30 secs to run.
# If I was hard pressed to do something different I would check if the sequence becomes periodic.
for i in range(len(numbers), 30000000):
    last = numbers[-1]
    new = 0
    if len(positions[last]) == 2:
        new = positions[last][1] - positions[last][0]
        positions[last].popleft()
    positions[new].append(len(numbers))
    numbers.append(new)
print(numbers[-1])
