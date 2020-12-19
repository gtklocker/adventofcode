import sys

second_part = True

rules, msgs = map(lambda s: s.split('\n'), sys.stdin.read().strip().split('\n\n'))
ruleset = {}

for rule in rules:
    lhs, rhs = rule.split(": ")
    if rhs[0]+rhs[-1] == '""':
        value = rhs[1:-1]
    else:
        value = [[int(x) for x in smol.split()] for smol in rhs.split(" | ")]
    ruleset[int(lhs)] = value

if second_part:
    ruleset[8] = [[42], [42, 8]]
    ruleset[11] = [[42, 31], [42, 11, 31]]

def matches(rule, string):
    if isinstance(ruleset[rule], str):
        return [string[len(ruleset[rule]):]] \
                if string[:len(ruleset[rule])] == ruleset[rule] else []
    results = []
    for subruleset in ruleset[rule]:
        subresults = [string]
        for subrule in subruleset:
            new_subresults = []
            for r in subresults:
                new_subresults.extend(matches(subrule, r))
            subresults = new_subresults
        results.extend(subresults)
    return results

ans = 0
for msg in msgs:
    rests = matches(0, msg)
    if '' in rests:
        ans += 1
print(ans)
