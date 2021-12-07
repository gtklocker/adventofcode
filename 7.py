import fileinput
xs = [int(x) for x in next(fileinput.input()).strip().split(',')]

ans = float('inf')
for i in range(min(xs), max(xs)+1):
    fuel = 0
    for j in xs:
        fuel += abs(i-j)*(abs(i-j)+1)//2
    ans = min(ans, fuel)
print(ans)
