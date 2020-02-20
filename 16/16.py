import numpy as np
import itertools
base_pattern = [0, 1, 0, -1]

def pattern_with_repetitions(rep):
    i, j = 0, 0
    while True:
        for _ in range(rep):
            yield (base_pattern[i], j)
            j += 1
        i = (i+1) % len(base_pattern)

def pattern_for_dim(dim):
    it = pattern_with_repetitions(dim+1)
    next(it)
    return it

def concrete_repetitions(n, dim):
    tile_num = (n // (dim+1)*4) + 1
    return np.tile(np.repeat(base_pattern, dim+1), tile_num)[1:n+1]

with open("input3.txt") as f:
    xs = np.array(list(map(int, f.readline().strip())))

msg_offset = xs[:7]
print('msg offset', msg_offset)
msg_offset = int(''.join(map(str, xs[:7])))
#d, m = msg_offset // len(xs), msg_offset % len(xs)
#print('msg offset: %dk + %d' % (d, m))
#
## TODO: maybe wrong boundaries
#initial = xs[m:m+8]
#print('initial:', initial)
#
#absolute_positions = [d*len(xs)+m+i for i in range(8)]

n = len(xs)
#print(np.array(list(itertools.islice(pattern_for_dim(0), n))))
#patterns = np.hstack([np.array(list(itertools.islice(pattern_for_dim(i), n))) for i in range(n)])
#print(patterns)
#
#for i in range(1):
#    xs = np.remainder(np.abs(np.dot(xs, patterns)), 10)
#print(xs)
#import sys
#sys.exit(0)

# 0, 1, 0, -1
# 0, 0, 1, 1, 0, 0, -1, -1

# 1, 2, 3, 4, 5, 6, 7
# 1, 0, -1, 0, 1, 0, -1 | phase = 1
# 0, 1, 1, 0, 0, -1, -1 | phase 2
#for phase in range(1, 10):
#    offset = phase-1 # skip leading zeros
#    sign = 1
#    ans = 0
#    for _ in range(phase):
#        offset += 1
#        ans += sign * xs[offset]
#    sign *= -1
#    offset += phase

print(list(itertools.islice(pattern_for_dim(0), 4*5)))

#period = 650
period = 4
#n = period*10000
n = period*5
prev_ans = xs
print(xs)
for phase in range(1, 10):
    ans = [0]*n
    for i in range(n):
        print('i:', i)
        # i-th digit
        #s = ''
        #pattern_loc_at_pos = {}
        for k, (mul, pattern_loc) in zip(range(n), pattern_for_dim(i)):
            #print(k, pattern_loc, mul)
            #identifier = (pattern_loc, k % period)
            #if identifier in pattern_loc_at_pos:
            #    print('cycle! i=%d, id=%s' % (i, identifier))
            #pattern_loc_at_pos[identifier] = ans[i]
            #_---
            #if k > 0 and pattern_loc % ((i+1)*4) == 1 and k % period == 0:
            #    print('k:', k)
            #    more = (n-k)//period
            #    ans[i] += ans[i]*more
            #    break
            #if len(prev_ans)<=k: 
            #    comp = prev_ans[k%period]
            #else:
            comp = prev_ans[k]
            ans[i] += mul * comp
        ans[i] = abs(ans[i]) % 10
        #s = s + '= %d' % ans[i]
        #print(s)
    prev_ans = ans
    print(ans)