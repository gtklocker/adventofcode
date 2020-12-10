import fileinput

nums = [int(line.strip()) for line in fileinput.input()]

ans1 = -1
for i in range(25, len(nums)):
    valid = False
    for j in range(i-25, i):
        for k in range(j+1, i):
            if nums[j]+nums[k] == nums[i]:
                valid = True
                break
        if valid:
            break
    if not valid:
        ans1 = nums[i]
        break

for i in range(len(nums)):
    cumsum = 0
    j = i
    min_num = float('inf')
    max_num = float('-inf')
    for j in range(i+1, len(nums)):
        cumsum += nums[j]
        min_num = min(min_num, nums[j])
        max_num = max(max_num, nums[j])
        if cumsum > ans1:
            break
        if cumsum == ans1:
            print(j-i, min_num+max_num)
            break
