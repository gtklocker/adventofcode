OPCODE_ADD = 1
OPCODE_MUL = 2
OPCODE_READ = 3
OPCODE_PRINT = 4
OPCODE_JUMP_IF_TRUE = 5
OPCODE_JUMP_IF_FALSE = 6
OPCODE_LT = 7
OPCODE_EQ = 8

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

def interpret_step(mem, ptr):
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
        store(int(input()))
    if opcode == OPCODE_PRINT:
        print(next_val())
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
    return mem, next_instruction_ptr()

def interpret(mem):
    ptr = 0
    while ptr is not None:
        mem, ptr = interpret_step(mem, ptr)
    return mem

with open("input.txt", "r") as f:
    interpret([int(x) for x in f.readline().split(',')])