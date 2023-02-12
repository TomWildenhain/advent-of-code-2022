import os

def read_input(day):
    with open("input%d.txt" % day, "rt") as f:
        return f.read().replace('\r', '')

def get_inp_lines(day):
    return [l.strip() for l in read_input(day).strip().split('\n')]

def part1():
    def score_outcome(x1, x2):
        if x1 == x2:
            return 3
        if (x1 + 1) % 3 == x2:
            return 6
        return 0
        
    def score_line(l):
        x1, x2 = ['ABCXYZ'.find(c) % 3 for c in l.split(' ')]
        return score_outcome(x1, x2) + x2 + 1
    print(sum(score_line(l) for l in get_inp_lines(2) if l))

def part2():
    def score_outcome(x1, x2):
        if x1 == x2:
            return 3
        if (x1 + 1) % 3 == x2:
            return 6
        return 0

    def get_x2(x1, res):
        if res == 0:
            return (x1 - 1) % 3
        if res == 2:
            return (x1 + 1) % 3
        return x1
        
    def score_line(l):
        x1, res = ['ABCXYZ'.find(c) % 3 for c in l.split(' ')]
        x2 = get_x2(x1, res)
        return score_outcome(x1, x2) + x2 + 1
    print(sum(score_line(l) for l in get_inp_lines(2) if l))

part2()