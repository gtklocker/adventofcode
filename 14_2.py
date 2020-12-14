import fileinput

lines = [line.strip().split(" = ") for line in fileinput.input()]

def applymask(mask, val):
    for i, m in enumerate(mask):
        off = 35-i
        if m == '1':
            val |= 1 << off
    return val

def decodexs(mask, val):
    for i, m in enumerate(mask):
        off = len(mask)-1-i
        if m == 'X':
            val1 = val | (1 << off)
            val0 = val & ((1 << 37) - 1 - (1 << off))
            yield from decodexs(mask[i+1:], val0)
            yield from decodexs(mask[i+1:], val1)
            break
    else:
        yield val

mem = {}
mask = None
for line in lines:
    loc, val = line
    if loc.startswith("mem["):
        memloc = int(loc[loc.index("[")+1:loc.index("]")])
        memloc = applymask(mask, memloc)
        for memloc in decodexs(mask, memloc):
            mem[memloc] = int(val)
    else:
        mask = val
print(sum(mem.values()))
