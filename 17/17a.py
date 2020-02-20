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
    while state[0] is not None:
        ptr, _ = state
        # TODO: lookahead hack to implement input stopping
        opcode, _ = parse_combined_opcode(mem[ptr])
        if opcode == OPCODE_READ:
            yield ('in', None)
        mem, state = interpret_step(mem, state, inps, outps)
        if opcode == OPCODE_PRINT:
            yield ('out', outps[-1])

def print_canvas(canvas):
    xs = [int(k.real) for k in canvas.keys()]
    ys = [int(k.imag) for k in canvas.keys()]
    lines = []
    for y in range(min(ys), max(ys)+1):
        line = []
        for x in range(min(xs), max(xs)+1):
            pt = x+y*1j
            line.append(canvas[pt] if pt in canvas else ' ')
        lines.append(''.join(line))
    print('\n'.join(lines))

canvas = {}
def play(mem):
    inps = deque([])
    pt = -1 
    for interrupt, v in interpret(mem, inps):
        v = chr(v)
        if v != '\n':
            pt += 1
        else:
            pt = -1+(pt.imag+1)*1j
            continue
        print(pt)
        canvas[pt] = v
        #print(v, end='')
    print()
    print_canvas(canvas)


with open("input.txt", "r") as f:
    mem = [int(x) for x in f.readline().split(',')]

play(mem)

def intersects(pt):
    return len([canvas[pt+p] for p in [1,-1,1j,-1j,0] if pt+p in canvas and canvas[pt+p] == '#']) == 5

def alignment_params(pt):
    return pt.real * pt.imag

s = 0
for pt in canvas:
    if intersects(pt):
        canvas[pt] = '*'
        align = alignment_params(pt)
        s += align
print(s)
print_canvas(canvas)