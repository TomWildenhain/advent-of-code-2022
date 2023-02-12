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
    lines = get_inp_lines(14)
    parts = [[[int(i) for i in p.split(',')] for p in l.split(' -> ')] for l in lines]
    mw = min(c[0] for p in parts for c in p)
    mh = min(c[1] for p in parts for c in p)
    w = max(c[0] for p in parts for c in p) - mw + 1
    h = max(c[1] for p in parts for c in p) + 1
    grid = [['.'] * w for _ in range(h)]
    parts = [[(x - mw, y) for x, y in p] for p in parts]
    print(w, h)
    print(mw, mh)

    def sign(x):
        if x < 0:
            return -1
        elif x > 0: 
            return 1
        return 0

    def draw_line(prev, coord):
        x1, y1 = prev
        x2, y2 = coord
        dx = sign(x2 - x1)
        dy = sign(y2 - y1)
        x, y = x1, y1
        while x != x2 or y != y2:
            grid[y][x] = '#'
            y += dy
            x += dx
        grid[y][x] = '#'

    for part in parts:
        prev = None
        for coord in part:
            if prev is not None:
                draw_line(prev, coord)
            prev = coord

    def print_grid():
        print('\n'.join(''.join(c for c in row) for row in grid))

    extra = set()
    def is_blocked(x, y):
        if y == h + 1:
            return True
        if y >= h or x - mw < 0 or x - mw >= w:
            return (x, y) in extra
        return grid[y][x - mw] != '.'

    def set_blocked(x, y):
        if y >= h or x - mw < 0 or x - mw >= w:
            extra.add((x, y))
            return
        grid[y][x - mw] = 'o'

    done = False
    cnt = 0
    while not is_blocked(500, 0) and not done:
        # print()
        # print_grid()
        # input()
        x, y = 500, 0
        while not done:
            if not is_blocked(x, y + 1):
                y += 1
            elif not is_blocked(x - 1, y + 1):
                y += 1
                x -= 1
            elif not is_blocked(x + 1, y + 1):
                y += 1
                x += 1
            else:
                set_blocked(x, y)
                cnt += 1
                break
            # if y >= h:
            #     done = True
    #print_grid()
    print(cnt)
        
        

part1()