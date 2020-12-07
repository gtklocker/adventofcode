import fileinput

lines = [line.strip() for line in fileinput.input()]
graph = {}
for line in lines:
    container, containees = line.split(" contain ")
    container = " ".join(container.split()[:-1])
    containees = [" ".join(con.split()[1:-1]) for con in containees.split(", ")]
    for c in containees:
        if c not in graph:
            graph[c] = []
        graph[c].append(container)

discovered = set()
def dfs(u):
    global discovered
    discovered.add(u)
    for v in graph.get(u, []):
        dfs(v)
dfs("shiny gold")
print(len(discovered)-1)
