import os
import re
from collections import defaultdict
from math import gcd

def read_input(day):
    with open("input%d.txt" % day, "rt") as f:
        return f.read().replace('\r', '')

def get_inp_lines(day):
    return [l.strip() for l in read_input(day).strip().split('\n')]

def part1():
    lines = get_inp_lines(15)
    parsed = [[int(x) for x in re.match('Sensor at x=([-\d]*), y=([-\d]*): closest beacon is at x=([-\d]*), y=([-\d]*)', l).groups()] for l in lines]
    #y = 10
    y = 2000000
    blocked = set()
    inrow = set()
    def fill(start, end):
        blocked.update(range(start, end + 1))

    for x1, y1, x2, y2 in parsed:
        d = abs(x2-x1) + abs(y2-y1)
        s = d - abs(y1-y)
        if s >= 0:
            start_x = x1 - s
            end_x = x1 + s
            fill(start_x, end_x)
        if y2 == y:
            inrow.add((x2, y2))

    print(len(blocked) - len(inrow))

def part2():
    import z3
    lines = get_inp_lines(15)
    parsed = [[int(x) for x in re.match('Sensor at x=([-\d]*), y=([-\d]*): closest beacon is at x=([-\d]*), y=([-\d]*)', l).groups()] for l in lines]
    solver = z3.Solver()
    x = z3.Int('x')
    y = z3.Int('y')
    def z3_abs(n):
        return z3.If(n >= 0,n,-n)
    max_val = 4000000
    solver.add(x <= max_val)
    solver.add(y <= max_val)
    solver.add(x >= 0)
    solver.add(y >= 0)
    for x1, y1, x2, y2 in parsed:
        d = abs(x2-x1) + abs(y2-y1)
        solver.add(z3_abs(x - x1) + z3_abs(y - y1) > d)
    print("Checking")
    print(solver.check())
    print(solver.model())
    m = solver.model()
    print(m.evaluate(x * 4000000 + y))

part2()