import fileinput
import numpy as np
xs = [int(x.strip()) for x in fileinput.input()]
print("part 1", sum(np.array(xs[1:]) - np.array(xs[:-1]) > 0))

ans = 0
_sum = sum(xs[:3])
for i in range(3, len(xs)):
    _new_sum = _sum - xs[i-3] + xs[i]
    if _new_sum > _sum:
        ans += 1
print("part 2", ans)
