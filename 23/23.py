from collections import deque, defaultdict, namedtuple
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
            if len(outps) % 3 == 0 and len(outps) > 0:
                yield ('out', outps[-3:])

Packet = namedtuple('Packet', ['sender', 'receiver', 'x', 'y'])

with open("input.txt") as f:
    mem = list(map(int, f.readline().strip().split(',')))
    machine_ids = range(50)
    inputs = [deque([i]) for i in machine_ids]
    pkt_queue = [deque([]) for _ in machine_ids]
    machines = [interpret(mem.copy(), inputs[i]) for i in machine_ids]
    nat_pkt = None
    nat_y_vals = set()
    for _ in itertools.count():
        idle = True
        for machine in machine_ids:
            print('machine:', machine)
            interrupt, v = next(machines[machine])
            if interrupt == 'in' and len(inputs[machine]) == 0:
                if len(pkt_queue[machine]) > 0:
                    idle = False
                    pkt = pkt_queue[machine].popleft()
                    inputs[machine].append(pkt.x)
                    assert next(machines[machine]) == ('in', None)
                    inputs[machine].append(pkt.y)
                else:
                    inputs[machine].append(-1)
            if interrupt == 'out':
                idle = False
                receiver, x, y = v
                if receiver == 255:
                    nat_pkt = Packet(sender=machine, receiver=0, x=x, y=y)
                else:
                    pkt = Packet(sender=machine, receiver=receiver, x=x, y=y)
                    pkt_queue[receiver].append(pkt)

        if not idle:
            continue
        if nat_pkt is not None:
            print('NAT:', nat_pkt)
            pkt_queue[0].append(nat_pkt)
            if nat_pkt.y in nat_y_vals:
                print('NAT dup:', nat_pkt)
                break
            else:
                nat_y_vals.add(nat_pkt.y)
                nat_pkt = None
