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
        ptr, _ = state
        # TODO: lookahead hack to implement input stopping
        opcode, _ = parse_combined_opcode(mem[ptr])
        if opcode == OPCODE_READ:
            yield ('in', None)
        mem, state = interpret_step(mem, state, inps, outps)
        if len(outps) - last_release == 3:
            yield ('out', tuple(outps[-3:]))
            last_release = len(outps)

TILE_EMPTY = 0
TILE_WALL = 1
TILE_BLOCK = 2
TILE_PADDLE = 3
TILE_BALL = 4
printable_char = {
    TILE_EMPTY: ' ',
    TILE_WALL: 'W',
    TILE_BLOCK: 'B',
    TILE_PADDLE: '_',
    TILE_BALL: 'O'
}

def print_canvas(canvas):
    xs = [int(k.real) for k in canvas.keys()]
    ys = [int(k.imag) for k in canvas.keys()]
    lines = []
    for y in range(min(ys), max(ys)+1):
        line = []
        for x in range(min(xs), max(xs)+1):
            pt = x+y*1j
            line.append(printable_char[canvas[pt]])
        lines.append(''.join(line))
    print('\n'.join(lines))

def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    return 0

def play(mem):
    mem = mem.copy()
    mem[0] = 2
    joystick = 0
    inputs = deque([])
    ball = 0+0j
    paddle = 0+0j
    score = 0
    canvas = defaultdict(lambda: 0)
    for kind, tpl in interpret(mem, inputs):
        if kind == 'in':
            inputs.append(joystick)
            continue
        x, y, tid = tpl
        pt = x + y*1j
        if pt == -1:
            score = tid
            continue
        canvas[pt] = tid
        if tid == TILE_PADDLE:
            paddle = pt
        if tid == TILE_BALL:
            ball = pt
            joystick = sign(ball.real - paddle.real)
    return score

def count_block_tiles(mem):
    block_tiles = set()
    for _, (x, y, tid) in interpret(mem.copy(), []):
        if tid == TILE_BLOCK: block_tiles.add(x+y*1j)
    return len(block_tiles)


with open("input.txt", "r") as f:
    mem = [int(x) for x in f.readline().split(',')]
    print(count_block_tiles(mem))
    print(play(mem))