import math
def eq(x, y):
    return abs(x-y) < 1e-7

asteroids = set()
for row_idx, line in enumerate(open("input.txt")):
    h = row_idx+1
    for col_idx, char in enumerate(line):
        w = col_idx+1
        if char == "#":
            asteroids.add((col_idx, row_idx))

def angle(a, b):
    a_ = (a[0], -a[1])
    b_ = (b[0], -b[1])
    ret = math.pi/2 - math.atan2(b_[1]-a_[1], b_[0]-a_[0])
    if ret < 0: ret += 2*math.pi
    return ret

def dist(a, b):
    return (a[1]-b[1])**2 + (a[0]-b[0])**2

def sorted_points_from(src):
    return sorted((angle(src, pt), dist(src, pt), pt) for pt in asteroids - {src})

def visible_asteroids_from(x):
    pts = sorted_points_from(x)
    count = 0
    prev_angle = 1e9
    for angle, _, pt in pts:
        if not eq(angle, prev_angle):
            count += 1
            prev_angle = angle
    return count

part_one, X = max((visible_asteroids_from(pt), pt) for pt in asteroids)
print(part_one, X)

vaporized = set()
prev_angle = 1e9
for angle, _, pt in sorted_points_from(X):
    if pt not in vaporized and not eq(angle, prev_angle):
        vaporized.add(pt)
        prev_angle = angle
        if len(vaporized) == 200:
            print(pt[0]*100 + pt[1])
            break