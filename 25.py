import fileinput
import itertools

card_pk, door_pk =  list(int(line.strip()) for line in fileinput.input())

def calc_target(subject, loop_size):
    return pow(subject, loop_size, 20201227)

def find_loop_size(target):
    x = 1
    for loop_size in itertools.count(1):
        x *= 7
        x %= 20201227
        if x == target:
            return loop_size

door_loop_size = find_loop_size(door_pk)
print(calc_target(card_pk, door_loop_size))
