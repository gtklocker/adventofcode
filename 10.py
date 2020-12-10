import fileinput

jolts = sorted([int(line.strip()) for line in fileinput.input()])
prev = 0
diffs = {1:0, 3:0}
for i in range(len(jolts)):
    diffs[jolts[i]-prev] += 1
    prev = jolts[i]
print(diffs[1]*(diffs[3]+1))

max_ = jolts[i]+3
dp = [0]*len(jolts)
for i in range(len(jolts)-1, -1, -1):
    if max_-jolts[i] <= 3:
        dp[i] = 1
    for j in range(i+1, len(jolts)):
        if jolts[j]-jolts[i] > 3:
            break
        dp[i] += dp[j]
print(sum(dp[:3]))
