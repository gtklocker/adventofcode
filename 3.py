inp = 265149

#acc = 0
#layer = 0
#while True:
#    row = 2*layer+1
#    nums = max(row*row - max((row-2)*(row-2), 0), 1)
#    if acc+nums >= inp:
#        print(layer, acc)
#        bkpts = [acc+1, acc+1+(row-1), acc+1+2*(row-1), acc+1+3*(row-1)]
#        print(bkpts)
#        if bkpts[0] <= inp <= bkpts[1]:
#            x = layer
#            y = -layer+1+(inp-bkpts[0])
#        elif bkpts[1] <= inp <= bkpts[2]:
#            y = layer
#            x = layer-1-(inp-bkpts[1])
#        elif bkpts[2] <= inp <= bkpts[3]:
#            x = -layer
#            y = layer+1+(inp-bkpts[2])
#        else:
#            y = -layer
#            x = -layer+1+(inp-bkpts[3])
#        print(abs(x)+abs(y))
#        break
#    acc += nums
#    layer += 1

n = 1001
ad = n // 2
mat = [[0 for _ in range(n)] for _ in range(n)]
x, y = 0, 0
mat[ad+x][ad+y] = 1
layer = 0
LEFT, RIGHT, UP, DOWN, NEXT = range(5)
direction = None
for _ in range(100):
    if (x,y) == (layer,-layer):
        direction = NEXT
    elif (x,y) == (layer,layer):
        direction = LEFT
    elif (x,y) == (layer,-layer+1):
        direction = UP
    elif (x,y) == (-layer,layer):
        direction = DOWN
    elif (x,y) == (-layer,-layer):
        direction = RIGHT

    if direction == LEFT:
        x -= 1
    elif direction == RIGHT:
        x += 1
    elif direction == UP:
        y += 1
    elif direction == DOWN:
        y -= 1
    elif direction == NEXT:
        x += 1
        layer += 1

    mat[ad+x][ad+y] = sum(mat[ad+x+dx][ad+y+dy] if 0 <= ad+x+dx < n and 0 <=ad+y+dy < n else 0 for dx in range(-1, 2) for dy in range(-1, 2))
    if mat[ad+x][ad+y] >= inp:
        print(mat[ad+x][ad+y])
        break
