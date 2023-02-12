import os
import re
from collections import defaultdict
from math import gcd
import functools

def read_input(day):
    with open("input%s.txt" % day, "rt") as f:
        return f.read().replace('\r', '')

def get_inp_lines(day):
    return [l.strip() for l in read_input(day).strip().split('\n')]

FACING_TO_DXY = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def part12(part=1):
    inpt = read_input(22)
    map, moves = inpt.split('\n\n')
    moves = moves.strip()
    moves = [m for m in moves.replace('L', ';L;').replace('R', ';R;').split(';') if m]
    rows = map.rstrip().split('\n')
    row_bounds = [(row.rfind(' ') + 1, len(row)-1) for row in rows]
    height = len(rows)
    width = max(len(row) for row in rows)
    col_bounds = []
    for x in range(width):
        start, end = None, None
        for y in range(height):
            if x < len(rows[y]) and rows[y][x] != ' ':
                if start is None:
                    start = y
                end = y
        col_bounds.append((start, end))

    if part == 1:
        # right, down, left, up
        warps = [{}, {}, {}, {}]
        for y, (sx, ex) in enumerate(row_bounds):
            warps[0][(ex + 1, y)] = ((sx, y), 0)
            warps[2][(sx - 1, y)] = ((ex, y), 2)
        for x, (sy, ey) in enumerate(col_bounds):
            warps[1][(x, ey + 1)] = ((x, sy), 1)
            warps[3][(x, sy - 1)] = ((x, ey), 3)

    elif part == 2:
        warps = make_warps_part2()

    y = 0
    x = rows[0].find('.')
    facing = 0
    for m in moves:
        if m == 'R':
            facing += 1
            facing %= 4
        elif m == 'L':
            facing -= 1
            facing %= 4
        else:
            n = int(m)
            for _ in range(n):
                dx, dy = FACING_TO_DXY[facing]
                nx = x + dx
                ny = y + dy
                nfacing = facing
                if (nx, ny) in warps[facing]:
                    (nx, ny), nfacing = warps[facing][(nx, ny)]
                if rows[ny][nx] != '#':
                    x, y, facing = nx, ny, nfacing
    print(x, y)
    print(1000 * (y + 1) + 4 * (x + 1) + facing)
    print(len(rows))

def make_warps_part2():
    warps = [{}, {}, {}, {}]

    links = [
        [((2, 0), 1, True), ((1, 1), 0, True)], # A
        [((1, 2), 0, True), ((2, 0), 0, False)], # B
        [((1, 1), 2, True), ((0, 2), 3, True)], # C
        [((0, 2), 2, False), ((1, 0), 2, True)], # D
        [((1, 0), 3, False), ((0, 3), 2, False)], # E
        [((0, 3), 0, False), ((1, 2), 1, False)], # F
        [((0, 3), 1, False), ((2, 0), 3, False)], # G
    ]

    def mk_rng(square, dir, inc):
        sx, sy = [(49, 0), (0, 49), (0, 0), (0, 0)][dir]
        sign = 1 if inc else -1
        dx = sign if dir in [1, 3] else 0
        dy = sign if dir in [0, 2] else 0
        if not inc and dx != 0:
            sx = 49 - sx
        if not inc and dy != 0:
            sy = 49 - sy
        x = 50 * square[0] + sx
        y = 50 * square[1] + sy
        for i in range(50):
            yield (x + i * dx, y + i * dy)

    def add_warps(r1, d1, r2, d2):
        dx, dy = FACING_TO_DXY[d1]
        d2 = (d2 + 2) % 4
        for (x1, y1), (x2, y2) in zip(r1, r2):
            warps[d1][(x1 + dx, y1 + dy)] = ((x2, y2), d2)

    for link in links:
        r1 = list(mk_rng(*link[0]))
        d1 = link[0][1]
        r2 = list(mk_rng(*link[1]))
        d2 = link[1][1]
        add_warps(r1, d1, r2, d2)
        add_warps(r2, d2, r1, d1)

    return warps

part12(2)