import fileinput
import itertools
from collections import defaultdict, Counter

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
foods = sorted(foods, key=lambda t: len(t[1]))
for ings, allergies in foods:
    for allergy in allergies:
        if allergy not in contains_allergy:
            contains_allergy[allergy] = []
        contains_allergy[allergy].append(ings)

reduced = {}
for allergy in contains_allergy:
    conj = contains_allergy[allergy][0]
    for ings in contains_allergy[allergy][1:]:
        conj &= ings
    reduced[allergy] = conj

possible = set.union(*reduced.values())
impossible = all_ings-possible
print(sum(appears[x] for x in impossible))
