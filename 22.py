import sys
from collections import deque

players = list(map(lambda s: deque([int(x) for x in s.split('\n')[1:]]), sys.stdin.read().strip().split('\n\n')))
winner = None
def step():
    global winner
    winner = players[0][0] < players[1][0]
    players[winner].extend([players[winner].popleft(), players[~winner].popleft()])

while all(players):
    step()

print(sum((i+1)*v for i, v in enumerate(list(players[winner])[::-1])))
