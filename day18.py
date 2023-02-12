import os
import re
from collections import defaultdict
from math import gcd

def read_input(day):
    with open("input%d.txt" % day, "rt") as f:
        return f.read().replace('\r', '')

def get_inp_lines(day):
    return [l.strip() for l in read_input(day).strip().split('\n')]

def get_dxyz():
    for i in range(3):
        l = [0] * 3
        for d in [1, -1]:
            l[i] = d
            yield tuple(l)

def part1():
    lines = get_inp_lines(18)
    coords = set(tuple(int(i) for i in l.split(',')) for l in lines)
    cnt = 0
    for x, y, z in coords:
        for dx, dy, dz in get_dxyz():
            if (x + dx, y + dy, z + dz) not in coords:
                cnt += 1
    print(cnt)

def part2():
    lines = get_inp_lines(18)
    coords = set(tuple(int(i) for i in l.split(',')) for l in lines)
    space = [[[0] * 20 for _ in range(20)] for _ in range(20)]
    cnt = 0
    for x, y, z in coords:
        space[x][y][z] = 1

    def get_space(x, y, z):
        try:
            return space[x][y][z]
        except:
            return 2
    
    done = False
    # Unnecessarily deep nesting...
    while not done:
        done = True
        for x in range(20):
            for y in range(20):
                for z in range(20):
                    if space[x][y][z] == 0:
                        for dx, dy, dz in get_dxyz():
                            if get_space(x + dx, y + dy, z + dz) == 2:
                                space[x][y][z] = 2
                                done = False
                                break

    cnt = 0
    for x, y, z in coords:
        for dx, dy, dz in get_dxyz():
            if (x + dx, y + dy, z + dz) not in coords and get_space(x + dx, y + dy, z + dz) == 2:
                cnt += 1

    print(cnt)

part2()