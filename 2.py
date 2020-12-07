import fileinput

ans1 = 0
ans2 = 0
for line in fileinput.input():
    l, pas = line.split(": ")
    ll, req = l.split()
    mi, ma = map(int, ll.split("-"))
    if mi <= pas.count(req) <= ma:
        ans1 += 1
    if (pas[mi-1] == req) ^ (pas[ma-1] == req):
        ans2 += 1
print(ans2)
