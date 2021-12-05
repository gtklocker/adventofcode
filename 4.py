import fileinput
_input = '\n'.join([x.strip() for x in fileinput.input()]).split("\n\n")

def parse_board(s):
    lines = s.split('\n')
    return [[int(x) for x in line.strip().split()] for line in lines]

def score(boards, drawn, boards_avail):
    for bn, board in enumerate(boards):
        if bn not in boards_avail:
            continue
        def col(c):
            return [row[c] for row in board]
        board_set = set()
        for row in board:
            board_set |= set(row)
        for i in range(5):
            if set(board[i]) - set(drawn) == set() or set(col(i)) - set(drawn) == set():
                ans = drawn[-1]*sum(board_set-set(drawn))
                yield (bn, ans)

to_draw = [int(x) for x in _input[0].split(',')]
boards = [parse_board(x) for x in _input[1:]]

drawn = []
boards_avail = set(range(len(boards)))
ans = 0
for x in to_draw:
    drawn.append(x)
    for bn, _ans in score(boards, drawn, boards_avail):
        ans = _ans
        boards_avail -= set([bn])
print(ans)
