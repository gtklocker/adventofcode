def solve(check_fn):
    return sum(1 for i in range(171309, 643603+1) if check_fn(i))

def valid_one(num):
    digit = None
    adjacent_rule_satisfied = False
    while num > 0:
        prev_digit = digit
        digit = num % 10
        num //= 10
        if prev_digit is None: continue
        if prev_digit == digit:
            adjacent_rule_satisfied = True
        if prev_digit < digit:
            return False
    return adjacent_rule_satisfied

def valid_two(num):
    digit = None
    group_digit = None
    group_size = None
    adjacent_rule_satisfied = False
    while num > 0:
        prev_digit = digit
        digit = num % 10
        num //= 10
        if prev_digit is None: continue
        if prev_digit == digit:
            if group_digit == digit:
                group_size += 1
            else:
                group_size = 2
                group_digit = digit
        else:
            if group_digit is not None and group_size == 2:
                adjacent_rule_satisfied = True
        if prev_digit < digit:
            return False
    if group_digit is not None and group_size == 2:
        adjacent_rule_satisfied = True
    return adjacent_rule_satisfied

print(solve(valid_one))
print(solve(valid_two))