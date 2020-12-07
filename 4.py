from collections import Counter
import fileinput

ans = 0
for line in fileinput.input():
    sorted_words = [''.join(sorted(word)) for word in line.strip().split()]
    ct = Counter(sorted_words)
    invalid = False
    for word in ct:
        if ct[word] > 1:
            invalid = True
            break
    if not invalid:
        ans += 1

print(ans)
