from collections import defaultdict
import functools
import fileinput

lines = list(map(lambda s: s.strip(), fileinput.input()))
input_type = 0
i = 0
classes = []
my_ticket = []
nearby_tickets = []
while i < len(lines):
    line = lines[i]
    if line == '':
        input_type += 1
        i += 2
        continue
    elif input_type == 0:
        # classes
        cls, ranges = line.split(': ')
        ranges = ranges.split(' or ')
        ranges = [list(map(int, r.split('-'))) for r in ranges]
        classes.append((cls, ranges))
    elif input_type == 1:
        # your ticket
        my_ticket = list(map(int, line.split(',')))
    elif input_type == 2:
        # nearby tickets
        nearby_tickets.append(list(map(int, line.split(','))))
    i += 1

invalid_tickets = set()
for i, ticket in enumerate(nearby_tickets):
    for v in ticket:
        valid = False
        for cls, ranges in classes:
            for r0, r1 in ranges:
                if r0 <= v <= r1:
                    valid = True
                    break
            if valid:
                break
        if not valid:
            invalid_tickets.add(i)

remaining_tickets = [t for i,t in enumerate(nearby_tickets) if i not in invalid_tickets]
match_by_ticket = defaultdict(set)
for i, ticket in enumerate(remaining_tickets):
    for j, v in enumerate(ticket):
        for k, (cls, ranges) in enumerate(classes):
            matches = False
            for r0, r1 in ranges:
                if r0 <= v <= r1:
                    matches = True
                    break
            if matches:
                match_by_ticket[(i,j)].add(k)
m = len(remaining_tickets[0])
n = len(remaining_tickets)

results = []
for j in range(m):
    matches = sorted([match_by_ticket[(i, j)] for i in range(n)], key=len)
    result = functools.reduce(lambda a, b: a&b, matches)
    results.append((j, result))

final_places = {}
used = set()
for j, result in sorted(results, key=lambda x: len(x[1])):
    using = list(result-used)[0]
    final_places[using] = j
    print(j, final_places)
    used.add(using)
ans = 1
for j in range(m):
    if classes[j][0].startswith("departure"):
        print(classes[j][0])
        ans *= my_ticket[final_places[j]]
print(ans)
