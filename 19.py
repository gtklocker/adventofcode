import sys

rules, msgs = map(lambda s: s.split('\n'), sys.stdin.read().strip().split('\n\n'))

ruleset = {}
for rule in rules:
    lhs, rhs = rule.split(": ")
    if rhs[0]+rhs[-1] == '""':
        value = rhs[1:-1]
    else:
        value = [[int(x) for x in smol.split()] for smol in rhs.split(" | ")]
    ruleset[int(lhs)] = value

def matches(rule, string):
    #print(rule, string)
    if isinstance(ruleset[rule], str):
        #print('checking string eq')
        #print(string[:len(ruleset[rule])], 'vs', string)
        if string[:len(ruleset[rule])] == ruleset[rule]:
            return True, string[len(ruleset[rule]):]
        else:
            return False, ""
    for subruleset in ruleset[rule]:
        #print('processing subruleset', subruleset)
        m, rest = True, string
        for subrule in subruleset:
            if not m or rest == "":
                break
            m, rest = matches(subrule, rest)
        if m:
            return True, rest
    return False, ""

ans = 0
for msg in msgs:
    m, rest = matches(0, msg)
    if m and rest == "":
        ans += 1
print(ans)
