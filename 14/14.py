from math import ceil

def parse_el(s):
    a, b = s.split(" ")
    return int(a), b

required_for = {}
for line in open("input.txt"):
    deps, prods = (s.strip().split(", ") for s in line.strip().split("=>"))
    deps = tuple(map(parse_el, deps))
    prod = tuple(map(parse_el, prods))[0]
    required_for[prod[1]] = (prod[0], deps)

def get_ore_required_for_fuel(f):
    requirements = {"FUEL": f}
    while not all(m == 'ORE' for m, a in requirements.items() if a > 0):
        metal, amount = next(((m, a) for m, a in requirements.items() if a > 0 and m != 'ORE'))

        amount_produced, deps = required_for[metal]
        times = ceil(amount / amount_produced)

        for amount, dep in deps:
            if dep not in requirements:
                requirements[dep] = 0
            requirements[dep] += times*amount

        requirements[metal] -= times*amount_produced
        if requirements[metal] == 0:
            del requirements[metal]
    return requirements['ORE']

def get_max_fuel_for_ore(target):
    lo, hi = 1, 1
    f = get_ore_required_for_fuel
    while True:
        ans = f(hi)
        if ans >= target:
            break
        hi *= 2

    while lo < hi:
        mid = (lo+hi)//2
        if f(mid) >= target:
            hi = mid
        else:
            lo = mid+1
    return lo-1

print(get_ore_required_for_fuel(1))
print(get_max_fuel_for_ore(10**12))