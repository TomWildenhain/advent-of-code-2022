import os
import re
from collections import defaultdict

def read_input(day):
    with open("input%d.txt" % day, "rt") as f:
        return f.read().replace('\r', '')

def get_inp_lines(day):
    return [l.strip() for l in read_input(day).strip().split('\n')]

class Directory:
    def __init__(self):
        self.dirs = defaultdict(Directory)
        self.files = {}
        self.size = 0

    def update_size(self):
        self.size = sum(d.update_size() for d in self.dirs.values()) + sum(self.files.values())
        return self.size

    def traverse(self):
        return [self] + [c for d in self.dirs.values() for c in d.traverse()]

def part1():
    root = Directory()
    pwd = [root]

    for l in get_inp_lines(7):
        if l.startswith('$ '):
            match l.split(' '):
                case ['$', 'cd', '/']:
                    pwd = [root]
                case ['$', 'cd', '..']:
                    pwd.pop()
                case ['$', 'cd', name]:
                    pwd.append(pwd[-1].dirs[name])
                case ['$', 'ls']:
                    pass
        else:
            t, n = l.split(' ')
            if t == 'dir':
                pwd[-1].dirs[n]
            else:
                pwd[-1].files[n] = int(t)

    root.update_size()
    small_children = sum(d.size for d in root.traverse() if d.size <= 100000)
    print(small_children)
    available = 70000000 - root.size
    needed = 30000000 - available
    smallest_working = min(d.size for d in root.traverse() if d.size >= needed)
    print(smallest_working)


part1()