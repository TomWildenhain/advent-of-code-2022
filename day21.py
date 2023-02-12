import os
import re
from collections import defaultdict
from math import gcd
import functools
import z3

def read_input(day):
    with open("input%s.txt" % day, "rt") as f:
        return f.read().replace('\r', '')

def get_inp_lines(day):
    return [l.strip() for l in read_input(day).strip().split('\n')]

OP_MAP = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x // y,
}

class Monkey:
    def __init__(self, line):
        self.name = None
        self.number = None
        self.op = None
        self.inputs = []
        parsed = re.match("(\w*): (\d+)", line)
        if parsed:
            self.name, self.number = parsed.groups()
            self.number = int(self.number)
        else:
            self.name, inp1, self.op, inp2 = re.match("(\w*): (\w*) (.) (\w*)", line).groups()
            self.inputs = [inp1, inp2]
        self.line = line
        self.symbol = z3.Int(self.name)

    def add_constraint(self, solver):
        if self.number is not None:
            solver.add(self.symbol == self.number)
        elif self.op == '/':
            inp1, inp2 = [inp.symbol for inp in self.inputs]
            solver.add(inp1 == inp2 * self.symbol)
        else:
            solver.add(self.symbol == OP_MAP[self.op](*[inp.symbol for inp in self.inputs]))

    def compute(self):

        if self.number is None:
            self.number = OP_MAP[self.op](*[inp.number for inp in self.inputs])

    def __repr__(self):
        return self.line

def topological_sort(dependencies):
    """
    Given a dictionary mapping items to lists of dependencies, returns a topological ordering of the items.
    Raises a ValueError for cyclic dependencies.
    """
    stack = list(dependencies.keys())
    visiting = set()
    visited = set()
    ordered = []
    while stack:
        x = stack.pop()
        if x in visited:
            continue
        if x in visiting:
            visiting.remove(x)
            visited.add(x)
            ordered.append(x)
            continue
        stack.append(x)
        visiting.add(x)
        for y in dependencies[x]:
            if y in visiting:
                raise ValueError("Cyclic dependencies present: %r" % dependencies)
            if y not in visited:
                stack.append(y)
    return ordered

def part1():
    monkeys = [Monkey(m) for m in get_inp_lines(21)]
    name_to_monkey = {m.name: m for m in monkeys}
    for m in monkeys:
        m.inputs = [name_to_monkey[inp] for inp in m.inputs]
    deps = {m: m.inputs for m in monkeys}
    sorted_ms = topological_sort(deps)
    for m in sorted_ms:
        m.compute()
    print(name_to_monkey['root'].number)

def part2():
    solver = z3.Solver()
    monkeys = [Monkey(m) for m in get_inp_lines(21)]
    name_to_monkey = {m.name: m for m in monkeys}
    for m in monkeys:
        m.inputs = [name_to_monkey[inp] for inp in m.inputs]
    for m in monkeys:
        if m.name == 'root':
            solver.add(m.inputs[0].symbol == m.inputs[1].symbol)
        elif m.name != 'humn':
            m.add_constraint(solver)
    print("Checking!")
    print(solver.check())
    m = solver.model()
    print(m.evaluate(name_to_monkey['humn'].symbol))
    

part2()