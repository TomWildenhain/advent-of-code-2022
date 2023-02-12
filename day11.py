import os
import re
from collections import defaultdict
from math import gcd

def read_input(day):
    with open("input%d.txt" % day, "rt") as f:
        return f.read().replace('\r', '')

def get_inp_lines(day):
    return [l.strip() for l in read_input(day).split('\n')]

def chunk(l, size=7):
    chunk = []
    for x in l:
        chunk.append(x)
        if len(chunk) == size:
            yield chunk
            chunk = []

class Monkey:
    def __init__(self, lines):
        self.inspect = 0
        self.items = [int(item) for item in lines[1][len("Starting items: "):].split(', ')]
        self.operation = lines[2][len("Operation: new = "):]
        self.div_test = int(lines[3][len("Test: divisible by "):])
        self.true_monkey = int(lines[4][len("If true: throw to monkey "):])
        self.false_monkey = int(lines[5][len("If false: throw to monkey "):])

def part1():
    lines = get_inp_lines(11)
    monkeys = [Monkey(c) for c in chunk(lines)]
    print(len(monkeys))

    for _ in range(20):
        for m in monkeys:
            for i in m.items:
                i = eval(m.operation, None, {'old': i})
                m.inspect += 1
                i //= 3
                target = m.true_monkey if i % m.div_test == 0 else m.false_monkey
                monkeys[target].items.append(i)
            m.items = []
    
    a, b = sorted(m.inspect for m in monkeys)[::-1][:2]
    print(a * b)

def part2():
    lines = get_inp_lines(11)
    monkeys = [Monkey(c) for c in chunk(lines)]
    print(len(monkeys))

    for c in range(10000):
        for m in monkeys:
            for i in m.items:
                i = eval(m.operation, None, {'old': i})
                m.inspect += 1
                i %= 9699690
                target = m.true_monkey if i % m.div_test == 0 else m.false_monkey
                monkeys[target].items.append(i)
            m.items = []
    
    a, b = sorted(m.inspect for m in monkeys)[::-1][:2]
    print(a * b)

part2()