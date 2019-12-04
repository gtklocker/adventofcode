def valid(num):
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

def solve_one():
    return sum(1 for i in range(171309, 643603+1) if valid(i))

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

def solve_two():
    return sum(1 for i in range(171309, 643603+1) if valid_two(i))

print(solve_one())
print(solve_two())