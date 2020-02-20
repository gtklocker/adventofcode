import numpy as np

positions = []
for line in open("input.txt"):
    clean_line = line.strip()[1:-1]
    coords = np.array([0]*3)
    for i, assign in enumerate(clean_line.split(", ")):
        _, value = assign.split("=")
        coords[i] = int(value)
    positions.append(coords)

n = len(positions)
velocities = [np.array([0]*3) for _ in range(n)]

def print_world():
    for i in range(n):
        print('pos', positions[i], 'vel', velocities[i])
    print("----")

rep = [0]*3
DIMS=3
for dim in range(DIMS):
    zs = [pos[dim] for pos in positions]
    vzs = [vel[dim] for vel in velocities]
    print(zs, vzs)
    def freeze():
        return (tuple(zs), tuple(vzs))
    NUM_STEPS = 10**9
    states = set()
    for t in range(NUM_STEPS+1):
        #print(zs, vzs)
        state = freeze()
        if state not in states:
            states.add(state)
        else:
            print('found repetition at step', t)
            print(zs, vzs)
            rep[dim] = t
            break
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
            
                dist = zs[j]-zs[i]
                vzs[i] += dist // abs(dist) if dist != 0 else 0
        
        for i in range(n):
            zs[i] += vzs[i]

print(rep)

from collections import defaultdict
def prime_factors(x):
    i = 2
    factors = defaultdict(lambda: 0)
    while i <= x:
        if x % i == 0:
            factors[i] += 1
            x //= i
        else:
            i += 1
    return factors

def divides_all(xs):
    fac = [prime_factors(x) for x in xs]
    bases = set()
    ret = 1
    for fa in fac:
        bases |= fa.keys()
    print(bases)
    for base in bases:
        exponent = max(fa[base] for fa in fac)
        print(base, exponent)
        ret *= base**exponent
    return ret

print(divides_all(rep))