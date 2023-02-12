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

def part1():
    grid = get_inp_lines(24)
    height = len(grid)
    width = len(grid[0])
    lefts = set()
    rights = set()
    ups = set()
    downs = set()
    sets = {
        '<': lefts,
        '>': rights,
        '^': ups,
        'v': downs,
    }
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c in sets:
                sets[c].add((x, y))

    def shortest_path(start_round, start, end):
        round = start_round
        reachable = set([start])

        def add_point(point, dxy):
            x, y = point
            dx, dy = dxy
            return (x + dx, y + dy)

        def has_blizzard(bset, dxy, point, mod):
            dx, dy = dxy
            x, y = point
            r = round % mod
            p1 = (x - dx * r, y - dy * r)
            p2 = add_point(p1, (dx * mod, dy * mod))
            p3 = add_point(p1, (-dx * mod, -dy * mod))
            if p1 in bset or p2 in bset or p3 in bset:
                return True
            return False

        def is_clear(point):
            x, y = point
            if not (0 <= x < width and 0 <= y < height):
                return False
            if grid[y][x] == '#':
                return False
            for dxy, c, mod in [((-1, 0), '<', width - 2), ((1, 0), '>', width - 2), ((0, -1), '^', height - 2), ((0, 1), 'v', height - 2)]:
                if has_blizzard(sets[c], dxy, point, mod):
                    return False
            return True

        def print_clear():
            lines = []
            for y in range(height):
                lines.append(''.join('.' if is_clear((x, y)) else 'X' for x in range(width)))
            print('\n'.join(lines))
            print()

        while True:
            round += 1
            next_reachable = set()
            for point in reachable:
                for dxy in [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]:
                    new_point = add_point(point, dxy)
                    if is_clear(new_point):
                        next_reachable.add(new_point)
            reachable = next_reachable
            if end in reachable:
                break
        return round

    start = (1, 0)
    end = (width - 2, height - 1)
    r2 = shortest_path(0, start, end)
    print(r2)
    r3 = shortest_path(r2, end, start)
    print(r3)
    r4 = shortest_path(r3, start, end)
    print(r4)

part1()