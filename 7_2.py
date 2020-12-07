import fileinput

lines = [line.strip() for line in fileinput.input()]
graph = {}
for line in lines:
    container, containees = line.split(" contain ")
    container = " ".join(container.split()[:-1])
    containees = [" ".join(con.split()[:-1]) for con in containees.split(", ")]
    for c in containees:
        if c == "no other":
            continue
        if container not in graph:
            graph[container] = []
        spl = c.split()
        num = int(spl[0])
        name = " ".join(spl[1:])
        graph[container].append((num, name))

ans = -1
def dfs(n, u):
    global ans
    ans += n
    for v in graph.get(u, []):
        dfs(n*v[0], v[1])
dfs(1, "shiny gold")
print(ans)
