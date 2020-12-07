import fileinput

lines = [line.strip() for line in fileinput.input()]
rev_graph = {}
fwd_graph = {}
for line in lines:
    container, containees = line.split(" contain ")
    container = " ".join(container.split()[:-1])
    containees = [" ".join(con.split()[:-1]) for con in containees.split(", ")]
    fwd_graph.setdefault(container, [])
    for c in containees:
        if c == "no other":
            continue
        spl = c.split()
        num = int(spl[0])
        name = " ".join(spl[1:])
        fwd_graph[container].append((num, name))
        rev_graph.setdefault(name, [])
        rev_graph[name].append(container)

discovered = set()
def dfs_p1(u):
    global discovered
    discovered.add(u)
    for v in rev_graph.get(u, []):
        dfs_p1(v)
dfs_p1("shiny gold")
print(len(discovered)-1)

ans = -1
def dfs_p2(n, u):
    global ans
    ans += n
    for v in fwd_graph.get(u, []):
        dfs_p2(n*v[0], v[1])
dfs_p2(1, "shiny gold")
print(ans)
