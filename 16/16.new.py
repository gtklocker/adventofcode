from functools import lru_cache
import sys
sys.setrecursionlimit(10**9)

@lru_cache()
def factor(i, k):
    where = ((k+1) % (4*(i+1))) // (i+1)
    return [0, 1, 0, -1][where]

#xs = [1,2,3,4,5,6,7,8]
xs = list(map(int, '03036732577212944063491565474664'))
print(xs)
n = len(xs)*10000

offset = int(''.join(map(str, xs[:7])))
print(offset)

@lru_cache(maxsize=None)
def result(i, level):
    #print(i, level)
    if level == 0:
        return xs[i%len(xs)]
    return abs(sum(component(i, k, level) for k in range(i, n))) % 10

@lru_cache(maxsize=None)
def component(i, k, level):
    print('component(i=', i, ', k=', k, ', level=', level, ')')
    f = factor(i, k)
    if f == 0: return 0
    return f * result(k, level-1)

#for offs in range(offset, offset+8):
#        values = {}
#        for k in range(n):
#            f = factor(offs, k)
#            if f not in values:
#                    values[f] = 0
#            values[f] += 1
#        print(values)
print(result(offset, 2))
