from collections import deque, defaultdict
import itertools

OPCODE_ADD = 1
OPCODE_MUL = 2
OPCODE_READ = 3
OPCODE_PRINT = 4
OPCODE_JUMP_IF_TRUE = 5
OPCODE_JUMP_IF_FALSE = 6
OPCODE_LT = 7
OPCODE_EQ = 8
OPCODE_REL_BASE = 9
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
PARAM_RELATIVE = 2

def interpret_step(mem, state, inputs, outputs):
    ptr, rel_base = state
    opcode, params = parse_combined_opcode(mem[ptr])
    offset = 0
    def ensure_exists(loc):
        assert loc >= 0
        if len(mem)-1 < loc:
            mem.extend([0] * (loc-len(mem)+1))
    def next_loc():
        nonlocal offset; offset += 1
        mode = params[offset-1]
        if mode == PARAM_POSITION:
            loc = mem[ptr+offset]
        elif mode == PARAM_IMMEDIATE:
            loc = ptr+offset
        elif mode == PARAM_RELATIVE:
            loc = mem[ptr+offset] + rel_base
        ensure_exists(loc)
        return loc
    def next_val():
        return mem[next_loc()]
    def store(x):
        mem[next_loc()] = x
        assert params[offset-1] != PARAM_IMMEDIATE
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
            return mem, (b, rel_base)
    if opcode == OPCODE_LT:
        x, y = next_val(), next_val()
        store(1 if x < y else 0)
    if opcode == OPCODE_EQ:
        x, y = next_val(), next_val()
        store(1 if x == y else 0)
    if opcode == OPCODE_HALT:
        return mem, (None, rel_base)
    if opcode == OPCODE_REL_BASE:
        rel_base += next_val()
    return mem, (next_instruction_ptr(), rel_base)

def interpret(mem, inps):
    ptr = 0
    outps = []
    state = (0, 0) # (ptr, rel_base)
    last_release = 0
    while state[0] is not None:
        mem, state = interpret_step(mem, state, inps, outps)
        if len(outps) - last_release == 2:
            yield tuple(outps[-2:])
            last_release = len(outps)

LEFT90, RIGHT90 = 0, 1
def rot(delta, rotation):
    if rotation == LEFT90:
        return delta * 1j**3
    return delta * 1j

def print_canvas(space):
    min_x = int(min(k.real for k in space.keys()))
    max_x = int(max(k.real for k in space.keys()))
    min_y = int(min(k.imag for k in space.keys()))
    max_y = int(max(k.imag for k in space.keys()))
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            print(' ' if space[x+y*1j] == BLACK else '*', end='')
        print()

BLACK, WHITE = 0, 1
def solve(mem):
    inputs = deque([WHITE])
    pos = 0+0j
    delta = 0-1j
    space = defaultdict(lambda: BLACK)
    stream = interpret(mem, inputs)
    for color, rotation in stream:
        space[pos] = color
        delta = rot(delta, rotation)
        pos += delta
        inputs.append(space[pos])
    print_canvas(space)
    print(len(space))

with open("input.txt", "r") as f:
    mem = [int(x) for x in f.readline().split(',')]
    solve(mem)