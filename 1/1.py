def fuel_easy(x):
    return x // 3 - 2
def fuel_hard(x):
    new_mass = fuel_easy(x)
    if new_mass <= 0: return 0
    return new_mass + fuel_hard(new_mass)

with open("input.txt") as f:
    masses = [int(n) for n in f]
    print(sum(map(fuel_easy, masses)))
    print(sum(map(fuel_hard, masses)))