import fileinput
from collections import Counter
state = [int(x) for x in next(fileinput.input()).strip().split(',')]

num_days = 256
cnt = Counter(state)
for days in range(1, num_days+1):
    zeroes = cnt[0]
    for i in range(1,9):
        cnt[i-1] = cnt[i]
    cnt[6] += zeroes
    cnt[8] = zeroes
print(sum(cnt.values()))
