import fileinput
from collections import Counter

foods = []
all_ings = set()
appears = Counter()

for line in fileinput.input():
    lhs, rhs = line.strip().strip(")").split(" (contains ")
    ing = set(lhs.split())
    allergies = set(rhs.split(", "))
    all_ings |= ing
    appears.update(ing)
    foods.append((ing, allergies))

contains_allergy = {}
for ings, allergies in foods:
    for allergy in allergies:
        if allergy not in contains_allergy:
            contains_allergy[allergy] = set(ings)
        contains_allergy[allergy] &= ings

impossible = all_ings - set.union(*contains_allergy.values())
print(sum(appears[x] for x in impossible))

used = set()
final_assignment = {}
while len(final_assignment) != len(contains_allergy):
    for allergen, possible in contains_allergy.items():
        rem = possible-used
        if len(rem) == 1:
            final_assignment[allergen] = next(iter(rem))
            used.add(final_assignment[allergen])
print(','.join(x[1] for x in sorted(final_assignment.items())))
