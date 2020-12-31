import math
import fileinput

inp = fileinput.input()
arrival = int(next(inp))
buses = [int(x) if x != 'x' else None for x in next(inp).strip().split(',')]

earliest = None
earliest_bus = None
for bus in buses:
    if bus is None:
        continue
    time = (arrival // bus) * bus
    if arrival % bus != 0:
        time += bus
    if earliest is None or time < earliest:
        earliest = time
        earliest_bus = bus
print(earliest_bus*(earliest-arrival))

guess = buses[0]
prod = buses[0]
for i, bus in enumerate(buses):
    if i == 0 or bus is None:
        continue
    while (guess+i) % bus != 0:
        guess += prod
    prod *= bus
print(guess)
