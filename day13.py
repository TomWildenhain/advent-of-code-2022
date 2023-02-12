import os
import re
from collections import defaultdict
from math import gcd

def read_input(day):
    with open("input%d.txt" % day, "rt") as f:
        return f.read().replace('\r', '')

def get_inp_lines(day):
    return [l.strip() for l in read_input(day).strip().split('\n')]

def compare(p1, p2):
    if isinstance(p1, int) and isinstance(p2, int):
        if p1 < p2:
            return -1
        elif p1 > p2:
            return 1
        else:
            return 0
    p1, p2 = [[p] if isinstance(p, int) else p for p in [p1, p2]]
    for s1, s2 in zip(p1, p2):
        c = compare(s1, s2)
        if c != 0:
            return c
    return compare(len(p1), len(p2))

def part1():
    pairs = [[eval(line) for line in chunk.split('\n')] for chunk in read_input(13).strip().split('\n\n')]
    print(sum(i + 1 if compare(p1, p2) < 1 else 0 for i, (p1, p2) in enumerate(pairs)))

class Packet:
    def __init__(self, data):
        self.data = data
    
    def __lt__(self, other):
        return compare(self.data, other.data) < 0

def part2():
    packets = [Packet(eval(line)) for line in read_input(13).split('\n') if line]
    packets.append(Packet([[2]]))
    packets.append(Packet([[6]]))
    packets.sort()
    packets = [p.data for p in packets]
    i1 = packets.index([[2]])
    i2 = packets.index([[6]])
    print((i1 + 1) * (i2 + 1))

part2()