import fileinput

lines = [line.strip().split(" = ") for line in fileinput.input()]

def applymask(mask, val):
    for i, m in enumerate(mask):
        off = 35-i
        if m == '1':
            val |= 1 << off
        if m == '0':
            val &= (1 << 37) - 1 - (1 << off)
    return val

mem = {}
mask = None
for line in lines:
    loc, val = line
    if loc.startswith("mem["):
        memloc = int(loc[loc.index("[")+1:loc.index("]")])
        mem[memloc] = applymask(mask, int(val))
    else:
        mask = val
print(sum(mem.values()))
