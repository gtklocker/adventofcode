import fileinput

xs = [x.strip() for x in fileinput.input()]

def most_common(rows, col):
    return int(len([1 for row in rows if row[col] == '1']) >= len(rows)/2)

def least_common(rows, col):
    return 1-most_common(rows, col)

rows, cols = len(xs), len(xs[0])
gamma = 0
for i in range(cols):
    if most_common(xs, i) == 1:
        gamma += 1 << (cols-1-i)
epsilon = gamma ^ ((1 << cols) - 1)
print(gamma*epsilon)

def repeatedly_eliminate(common_fn):
    candidates = set(xs)
    for j in range(cols):
        m = common_fn(candidates, j)
        remove = set()
        for row in candidates:
            if int(row[j]) != m:
                remove.add(row)
        candidates -= remove
        if len(candidates) == 1:
            return int(candidates.pop(), 2)
oxygen, co2 = repeatedly_eliminate(most_common), repeatedly_eliminate(least_common)
print(oxygen*co2)
