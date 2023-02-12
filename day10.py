import os
import re
from collections import defaultdict

def read_input(day):
    with open("input%d.txt" % day, "rt") as f:
        return f.read().replace('\r', '')

def get_inp_lines(day):
    return [l.strip() for l in read_input(day).strip().split('\n')]

def part1():
    x = [1]
    c = [1]
    lines = get_inp_lines(10)
    strengths = []

    #20th, 60th, 100th, 140th, 180th, and 220th

    def complete_cycle():
        if c[0] in [20, 60, 100, 140, 180, 220]:
            strengths.append(x[0] * c[0])
        c[0] += 1

    for inst in lines:
        match inst.split(' '):
            case ['addx', v]:
                complete_cycle()
                complete_cycle()
                x[0] += int(v)
            case ['noop']:
                complete_cycle()

    print(c[0])
    print(sum(strengths))

def part2():
    x = [1]
    c = [1]
    lines = get_inp_lines(10)
    strengths = []

    #20th, 60th, 100th, 140th, 180th, and 220th

    data = [[]]

    def complete_cycle():
        if len(data[-1]) == 40:
            data.append([])
        col = len(data[-1])
        data[-1].append('#' if abs(col - x[0]) <= 1 else '.')
        c[0] += 1

    for inst in lines:
        match inst.split(' '):
            case ['addx', v]:
                complete_cycle()
                complete_cycle()
                x[0] += int(v)
            case ['noop']:
                complete_cycle()

    print(c[0])
    print('\n'.join(''.join(l for l in row) for row in data))


part2()