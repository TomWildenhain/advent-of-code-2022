import os
import re
from collections import defaultdict, Counter
from math import gcd
import itertools

def read_input(day):
    with open("input%s.txt" % day, "rt") as f:
        return f.read().replace('\r', '')

def get_inp_lines(day):
    return [l.strip() for l in read_input(day).strip().split('\n')]

class Elf:
    def __init__(self, pos):
        self.pos = pos
        self.target

def part1():
    rows = get_inp_lines(23)
    positions = set()
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c == '#':
                positions.add((x, y))
    print(len(positions))
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    def to_check(d):
        ds = [d]
        dx, dy = d
        if dx != 0:
            ds += [(dx, 1), (dx, -1)]
        if dy != 0:
            ds += [(1, dy), (-1, dy)]
        return ds

    def add(start, d):
        sx, sy = start
        dx, dy = d
        return (sx + dx, sy + dy)

    def is_empty(start, d):
        # print(start, d, positions, add(start, d), add(start, d) not in positions)
        return add(start, d) not in positions

    def all_empty(start):
        for dx, dy in itertools.product([-1, 0, 1], repeat=2):
            if (dx != 0 or dy != 0) and not is_empty(start, (dx, dy)):
                return False
        return True

    def can_move(start, d):
        return all(is_empty(start, c) for c in to_check(d))

    # print_grid(positions)
    print()

    done = False
    i = 0
    while not done:
        i += 1
        done = True
        moves = {}
        for elf in positions:
            if all_empty(elf):
                moves[elf] = elf
            else:
                for d in directions:
                    if can_move(elf, d):
                        moves[elf] = add(elf, d)
                        done = False
                        break
                else:
                    moves[elf] = elf

        assert len(positions) == len(moves)
        targeted = Counter(moves.values())
        new_positions = set()
        for elf, p in moves.items():
            if targeted[p] <= 1:
                new_positions.add(p)
            else:
                new_positions.add(elf)
        assert len(positions) == len(new_positions)
        positions = new_positions
        directions = directions[1:] + [directions[0]]

        # print_grid(positions)
        # print()

    min_x = min(p[0] for p in positions)
    min_y = min(p[1] for p in positions)
    max_x = max(p[0] for p in positions)
    max_y = max(p[1] for p in positions)
    # print((max_x - min_x + 1) * (max_y - min_y + 1) - len(positions))
    print(i)

def print_grid(positions):
    min_x = min(p[0] for p in positions)
    min_y = min(p[1] for p in positions)
    max_x = max(p[0] for p in positions)
    max_y = max(p[1] for p in positions)
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    grid = [['.'] * width for _  in range(height)]
    for x, y in positions:
        grid[y - min_y][x - min_x] = '#'
    print('\n'.join(''.join(c for c in row) for row in grid))

part1()