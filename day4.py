import os

def read_input(day):
    with open("input%d.txt" % day, "rt") as f:
        return f.read().replace('\r', '')

def get_inp_lines(day):
    return [l.strip() for l in read_input(day).strip().split('\n')]

def part1():
    def has_contained(bounds):
        a, b, c, d = bounds
        if a <= c and b >= d:
            return 1
        if c <= a and d >= b:
            return 1
        return 0

    print(sum(has_contained([int(b) for r in l.split(',') for b in r.split('-')]) for l in get_inp_lines(4)))

def part2():
    def has_contained(bounds):
        a, b, c, d = bounds
        if c <= b and a <= d:
            return 1
        return 0

    print(sum(has_contained([int(b) for r in l.split(',') for b in r.split('-')]) for l in get_inp_lines(4)))

part2()