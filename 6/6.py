def dfs(adj, nodes=None, desired_end=None):
    path_len = {}
    seen = set()
    def dfs_(adj, start):
        s = 1
        adj_nodes = adj.get(start, [])
        end = start
        seen.add(start)
        for node in adj_nodes:
            if node in seen:
                continue
            rest, their_end = dfs_(adj, node)
            if desired_end is None or their_end == desired_end:
                end = their_end
                s += rest
                if their_end == desired_end:
                    break
        return s, end
    nodes = nodes or adj.keys()
    for node in nodes:
        seen.clear()
        path_len[node] = dfs_(adj, node)[0]
    return path_len

def orbits_to_adj(orbits, oneway=True):
    adj = {}
    for orbit in orbits:
        if orbit[1] not in adj:
            adj[orbit[1]] = []
        adj[orbit[1]].append(orbit[0])
        if not oneway:
            if orbit[0] not in adj:
                adj[orbit[0]] = []
            adj[orbit[0]].append(orbit[1])
    return adj

def solve_one(orbits):
    adj = orbits_to_adj(orbits)
    path_len = dfs(adj)
    return sum(path_len[p]-1 for p in path_len)

def solve_two(orbits):
    adj = orbits_to_adj(orbits, False)
    path_len = dfs(adj, ['YOU'], 'SAN')
    return path_len['YOU']-2-1

with open("input.txt") as f:
    orbits = [line.strip().split(')') for line in f]
    print(solve_one(orbits))
    print(solve_two(orbits))