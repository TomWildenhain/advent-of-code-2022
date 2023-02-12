import os

def read_input(day):
    with open("input%d.txt" % day, "rt") as f:
        return f.read().replace('\r', '')

def get_inp_lines(day):
    return [l.strip for l in read_input(day).strip().split('\n')]

def part1():
    print(max(sum(int(l) for l in chunk.split('\n') if l) for chunk in read_input(1).split('\n\n')))

def part2():
    print(sum(sorted(sum(int(l) for l in chunk.split('\n') if l) for chunk in read_input(1).split('\n\n'))[-3:]))

part2()