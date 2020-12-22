import sys
from collections import deque

players = list(map(lambda s: deque([int(x) for x in s.split('\n')[1:]]), sys.stdin.read().strip().split('\n\n')))

def game(players):
    history = set()
    while all(players):
        if tuple(map(tuple, players)) in history:
            return players, 0
        history.add(tuple(map(tuple, players)))
        p1, p2 = players
        if any(p[0] > len(p)-1 for p in players):
            winner = players[0] < players[1]
        else:
            _, winner = game([deque(p[1:1+p[0]]) for p in map(list, players)])
        players[winner].extend([players[winner].popleft(), players[~winner].popleft()])
    return players, winner

players, winner = game(players)
print(sum((i+1)*v for i, v in enumerate(list(players[winner])[::-1])))
