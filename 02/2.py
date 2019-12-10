OPCODE_ADD = 1
OPCODE_MUL = 2

def interpret_step(mem, ptr):
    opcode = mem[ptr]
    if opcode in (OPCODE_ADD, OPCODE_MUL):
        x, y = mem[mem[ptr+1]], mem[mem[ptr+2]]
        if opcode == OPCODE_ADD: z = x + y
        if opcode == OPCODE_MUL: z = x * y
        mem[mem[ptr+3]] = z
        if ptr+4 < len(mem):
            return mem, ptr+4
    return mem, None

def interpret(mem):
    ptr = 0
    while ptr is not None:
        mem, ptr = interpret_step(mem, ptr)
    return mem

def first_part(mem):
    mem[1] = 12
    mem[2] = 2
    mem = interpret(mem)
    return mem[0]

def second_part(mem):
    desired_output = 19690720
    for mem[1] in range(100):
        for mem[2] in range(100):
            output = interpret(mem.copy())[0]
            if output == desired_output:
                return 100 * mem[1] + mem[2]

with open("input.txt", "r") as f:
    mem = [int(x) for x in f.readline().split(',')]
    print(first_part(mem.copy()))
    print(second_part(mem.copy()))