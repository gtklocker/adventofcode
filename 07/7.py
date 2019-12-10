from collections import deque
import itertools

OPCODE_ADD = 1
OPCODE_MUL = 2
OPCODE_READ = 3
OPCODE_PRINT = 4
OPCODE_JUMP_IF_TRUE = 5
OPCODE_JUMP_IF_FALSE = 6
OPCODE_LT = 7
OPCODE_EQ = 8
OPCODE_HALT = 99

def parse_combined_opcode(v):
    opcode = v % 100
    v //= 100
    param_mode = [0]*3
    for i in range(3):
        param_mode[i] = v % 10
        v //= 10
    return opcode, param_mode

PARAM_POSITION = 0
PARAM_IMMEDIATE = 1

def interpret_step(mem, ptr, inputs, outputs):
    opcode, params = parse_combined_opcode(mem[ptr])
    offset = 0
    def next_val():
        nonlocal offset; offset += 1
        if params[offset-1] == PARAM_POSITION:
            return mem[mem[ptr+offset]]
        else:
            return mem[ptr+offset]
    def store(x):
        nonlocal offset; offset += 1
        assert params[offset-1] != PARAM_IMMEDIATE
        mem[mem[ptr+offset]] = x
    def next_instruction_ptr():
        nonlocal offset; offset += 1
        if ptr+offset < len(mem):
            return ptr+offset
    if opcode in (OPCODE_ADD, OPCODE_MUL):
        x, y = next_val(), next_val()
        if opcode == OPCODE_ADD: z = x + y
        if opcode == OPCODE_MUL: z = x * y
        store(z)
    if opcode == OPCODE_READ:
        store(inputs.popleft())
    if opcode == OPCODE_PRINT:
        x = next_val()
        outputs.append(x)
    if opcode in (OPCODE_JUMP_IF_TRUE, OPCODE_JUMP_IF_FALSE):
        a, b = next_val(), next_val()
        true_sat = opcode == OPCODE_JUMP_IF_TRUE and a != 0
        false_sat = opcode == OPCODE_JUMP_IF_FALSE and a == 0
        if true_sat or false_sat:
            assert b < len(mem)
            return mem, b
    if opcode == OPCODE_LT:
        x, y = next_val(), next_val()
        store(1 if x < y else 0)
    if opcode == OPCODE_EQ:
        x, y = next_val(), next_val()
        store(1 if x == y else 0)
    if opcode == OPCODE_HALT:
        return mem, None
    return mem, next_instruction_ptr()

def interpret(mem, inputs):
    ptr = 0
    inps = deque(inputs)
    outps = []
    while ptr is not None:
        mem, ptr = interpret_step(mem, ptr, inps, outps)
    return outps

def run_amps(mem, conf):
    e = 0
    for c in conf:
        e = interpret(mem.copy(), [c, e])[0]
    return e

def run_amps_recur(mem, conf):
    inps = [deque([c]) for c in conf]
    outps = [[] for _ in conf]
    ptrs = [0 for _ in conf]
    mems = [mem.copy() for _ in conf]
    inps[0].append(0)
    while ptrs[-1] is not None:
        for i in range(len(conf)):
            size_outps = len(outps[i])
            while ptrs[i] is not None:
                mems[i], ptrs[i] = interpret_step(mems[i], ptrs[i], inps[i], outps[i])
                if len(outps[i]) > size_outps:
                    break
            new_outp = outps[i][-1]
            inps[(i+1)%len(conf)].append(new_outp)
    return new_outp

with open("input.txt", "r") as f:
    mem = [int(x) for x in f.readline().split(',')]
    all_confs_one = itertools.permutations(range(5))
    print(max(run_amps(mem, conf) for conf in all_confs_one))
    all_confs_two = itertools.permutations(range(5, 10))
    print(max(run_amps_recur(mem, conf) for conf in all_confs_two))