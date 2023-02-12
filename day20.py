import os
import re
from collections import defaultdict
from math import gcd
import functools
import numpy as np

def read_input(day):
    with open("input%s.txt" % day, "rt") as f:
        return f.read().replace('\r', '')

def get_inp_lines(day):
    return [l.strip() for l in read_input(day).strip().split('\n')]

class Node:
    def __init__(self, num):
        self.num = num

    def __repr__(self) -> str:
        return 'Node(%s)' % self.num

def part1():
    nums = [int(x) for x in get_inp_lines(20)]
    print(len(nums))
    nodes = [Node(x) for x in nums]
    sequence = nodes[:]
    m = len(nodes)
    zero, = [n for n in nodes if n.num == 0]
    # print(sequence)
    for n in nodes:
        i = sequence.index(n)
        before = sequence[:i]
        after = sequence[i+1:]
        # Rearrange from before, i, after to i, after, before
        s = n.num % (m - 1)
        combined = after + before
        part1, part2 = combined[:s], combined[s:]
        sequence = part1 + [n] + part2
        # print(sequence)
    zi = sequence.index(zero)
    before = sequence[:zi]
    after = sequence[zi+1:]
    sequence = [zero] + after + before
    # print(sequence)
    print(sum(sequence[i % m].num for i in [1000, 2000, 3000]))

def part2():
    nums = [int(x) * 811589153 for x in get_inp_lines(20)]
    print(len(nums))
    nodes = [Node(x) for x in nums]
    sequence = nodes[:]
    m = len(nodes)
    zero, = [n for n in nodes if n.num == 0]
    # print(sequence)
    for i in range(10):
        for n in nodes:
            i = sequence.index(n)
            before = sequence[:i]
            after = sequence[i+1:]
            # Rearrange from before, i, after to i, after, before
            s = n.num % (m - 1)
            combined = after + before
            part1, part2 = combined[:s], combined[s:]
            sequence = part1 + [n] + part2
        print(i)
    zi = sequence.index(zero)
    before = sequence[:zi]
    after = sequence[zi+1:]
    sequence = [zero] + after + before
    # print(sequence)
    print(sum(sequence[i % m].num for i in [1000, 2000, 3000]))

part2()