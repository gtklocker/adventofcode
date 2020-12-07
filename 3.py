import fileinput
import math

terrain = [x.strip() for x in fileinput.input()]
def trees_on_slope(right, down):
    j = right 
    ans = 0
    for i in range(down, len(terrain), down):
        if terrain[i][j] == "#":
            ans += 1
        j = (j+right) % len(terrain[i])
    return ans
print(math.prod(trees_on_slope(r, d) for r, d in ((1,1), (3,1), (5,1), (7,1), (1,2))))
