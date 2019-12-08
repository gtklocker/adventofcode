w, h = 25, 6
inp = open("input.txt").readline().strip()
layers = [[[-1 for _ in range(w)] for _ in range(h)] for _ in range(len(inp) // (w*h))]

for i in range(0, len(inp) // (w*h)):
    for y in range(h):
        for x in range(w):
            layers[i][y][x] = int(inp[i*w*h + y*w + x])

def count(layer, needle):
    return sum(row.count(needle) for row in layer)

BLACK = 0
WHITE = 1
TRANSPARENT = 2

def pixel(y, x):
    return next(layer[y][x] for layer in layers if layer[y][x] != TRANSPARENT)

least_zeros_layer = min(((count(layer, 0), layer) for layer in layers), key=lambda x:x[0])[1]
ans = count(least_zeros_layer, 1) * count(least_zeros_layer, 2)
print(ans)

for y in range(h):
    for x in range(w):
        p = pixel(y, x)
        print('*' if p == WHITE else ' ', end='')
    print()