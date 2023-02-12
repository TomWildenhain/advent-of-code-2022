import os
import re
from collections import defaultdict
from math import gcd

def read_input(day):
    with open("input%d.txt" % day, "rt") as f:
        return f.read().replace('\r', '')

def get_inp_lines(day):
    return [l.strip() for l in read_input(day).strip().split('\n')]

def part1():
    inf = float('inf')
    grid = get_inp_lines(12)
    w = len(grid[0])
    h = len(grid)
    def find_coord(target_c):
        coord, = [(y, x) for y, row in enumerate(grid) for x, c in enumerate(row) if c == target_c]
        return coord
    def get_elevation(y, x):
        return ord(grid[y][x].replace('S', 'a').replace('E', 'z')) - ord('a')
    dists = [[inf] * w for _ in range(h)]
    s_y, s_x = find_coord('S')
    e_y, e_x = find_coord('E')
    dists[s_y][s_x] = 0
    for y in range(h):
        for x in range(w):
            if grid[y][x] == 'a':
                dists[y][x] = 0
    print(h, w)
    change = True
    while change:
        #print(dists[s_y][20])
        change = False
        for y in range(h):
            for x in range(w):
                for dy in [-1, 0, 1]:
                    if not 0 <= y + dy < h:
                        continue
                    for dx in [-1, 0, 1]:
                        if (not (0 <= x + dx < w)) or (dx == 0 and dy == 0) or (dx != 0 and dy != 0):
                            continue
                        if get_elevation(y, x) <= get_elevation(y + dy, x + dx) + 1:
                            if 1 + dists[y + dy][x + dx] < dists[y][x]:
                                dists[y][x] = 1 + dists[y + dy][x + dx]
                                change = True
    print(dists[e_y][e_x])
    #print('\n'.join(''.join(str(d) for d in row) for row in dists))

part1()