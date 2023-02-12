import os
import re

def read_input(day):
    with open("input%d.txt" % day, "rt") as f:
        return f.read().replace('\r', '')

def get_inp_lines(day):
    return [l.strip() for l in read_input(day).strip().split('\n')]

def part1():
    lines = get_inp_lines(5)
    def parse_move(l):
        return re.match('move ([0-9]*) from ([0-9]*) to ([0-9]*)', l)
        
    top = lines[:9]
    stacks = [list(s[::-1]) for s in top]
    bottom = lines[10:]
    moves = [parse_move(l) for l in bottom]
    for m in moves:
        cnt, frm, to = [int(i) for i in m.groups()]
        for _ in range(cnt):
            stacks[to-1].append(stacks[frm-1].pop())
    print(''.join(s[-1] for s in stacks))

def part2():
    lines = get_inp_lines(5)
    def parse_move(l):
        return re.match('move ([0-9]*) from ([0-9]*) to ([0-9]*)', l)
        
    top = lines[:9]
    stacks = [list(s[::-1]) for s in top]
    bottom = lines[10:]
    moves = [parse_move(l) for l in bottom]
    for m in moves:
        cnt, frm, to = [int(i) for i in m.groups()]
        stacks[to-1] += stacks[frm-1][-cnt:]
        stacks[frm-1] = stacks[frm-1][:-cnt]
    print(''.join(s[-1] for s in stacks))

part2()