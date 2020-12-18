import fileinput
import math
import operator

def tokenize(expr):
    result = []
    for c in expr.split():
        if c in '+*':
            result.append(c)
            continue
        while c[0] == '(':
            result.append('(')
            c = c[1:]
        closing = c.find(')')
        if closing == -1:
            result.append(int(c))
        else:
            result.append(int(c[:closing]))
            c = c[closing:]
            while c and c[0] == ')':
                result.append(')')
                c = c[1:]
    return result

op_map = {
    '+': operator.add,
    '*': operator.mul,
}

def evaluate(expr):
    stack_nums = [[]]
    stack_ops = [[]]
    tokens = tokenize(expr)
    def push_num(num):
        if len(stack_ops[-1]) != 0 and (op := stack_ops[-1][-1]) == operator.add:
            stack_ops[-1].pop()
            stack_nums[-1].append(op(num, stack_nums[-1].pop()))
        else:
            stack_nums[-1].append(num)
    for token in tokens:
        if isinstance(token, int):
            push_num(token)
        elif token in '+*':
            stack_ops[-1].append(op_map[token])
        elif token == '(':
            stack_nums.append([])
            stack_ops.append([])
        elif token == ')':
            rem = stack_nums.pop()
            stack_ops.pop()
            push_num(math.prod(rem))
    return math.prod(stack_nums[-1])

ans = 0
for line in fileinput.input():
    expr = line.strip()
    ans += evaluate(expr)
print(ans)
