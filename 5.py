import fileinput

seats = [line.strip() for line in fileinput.input()]

rows = 128
cols = 8

seat_ids = []
for seat in seats:
    min_row, min_col = 0, 0
    max_row, max_col = rows, cols
    for c in seat:
        if c == 'F':
            max_row = (min_row+max_row) // 2
        if c == 'B':
            min_row = (min_row+max_row) // 2
        if c == 'L':
            max_col = (min_col+max_col) // 2
        if c == 'R':
            min_col = (min_col+max_col) // 2
    seat_id = min_row*8 + min_col
    seat_ids.append(seat_id)
seat_ids.sort()
for i, sid in enumerate(seat_ids):
    if i > 0 and sid-seat_ids[i-1] == 2:
        print(sid-1)
