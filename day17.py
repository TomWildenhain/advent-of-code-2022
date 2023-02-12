import os
import re
from collections import defaultdict
from math import gcd
import itertools

def read_input(day):
    with open("input%d.txt" % day, "rt") as f:
        return f.read().replace('\r', '')

def get_inp_lines(day):
    return [l.strip() for l in read_input(day).strip().split('\n')]

BLOCKS = """
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""

def loop(x):
    while True:
        for c in x:
            yield c

def part1():
    blocks = [b.strip().split('\n')[::-1] for b in BLOCKS.strip().split('\n\n')]
    chamber = []

    class State:
        def __init__(self):
            self.block_i = 0
            self.block_x = 2
            self.block_y = 3 + len(chamber)

    def is_empty(x, y):
        if 0 <= x < 7 and 0 <= y < len(chamber):
            return chamber[y][x] != '#'
        elif 0 <= x < 7 and y >= len(chamber):
            return True
        return False

    def can_push(b, new_x, new_y):
        for y, row in enumerate(b):
            for x, char in enumerate(row):
                if char == '#':
                    if not is_empty(new_x + x, new_y + y):
                        return False
        return True

    def fill_chamber(x, y):
        while len(chamber) <= y:
            chamber.append(['.'] * 7)
        chamber[y][x] = '#'

    def lock_block(b, block_x, block_y):
        for y, row in enumerate(b):
            for x, char in enumerate(row):
                if char == '#':
                    fill_chamber(block_x + x, block_y + y)

    def get_depths():
        depths = []
        for x in range(7):
            d = 0
            while is_empty(x, len(chamber) - d):
                d += 1
            depths.append(d)
        return tuple(depths)

    s = State()
    dir_map = {'<': -1, '>': 1}
    base = None
    locked_cnt = 0
    commands = read_input(17).strip()
    i = 0
    seen = {}
    terminate = None
    heights = [0]
    while True:
        dx = dir_map[commands[i]]
        if can_push(blocks[s.block_i], s.block_x + dx, s.block_y):
            s.block_x += dx
        if can_push(blocks[s.block_i], s.block_x, s.block_y - 1):
            s.block_y -= 1
        else:
            lock_block(blocks[s.block_i], s.block_x, s.block_y)
            locked_cnt += 1
            s.block_i = (s.block_i + 1) % len(blocks)
            s.block_x = 2
            s.block_y = 3 + len(chamber)
            heights.append(len(chamber))
            # if locked_cnt == 35:
            #     print('\n'.join(''.join(row) for row in chamber[-10:][::-1]))
            #     print('-----------------')
            # if locked_cnt == 1760:
            #     print('\n'.join(''.join(row) for row in chamber[-10:][::-1]))
            #     break
            key = (s.block_i, i, get_depths())
            if key in seen:
                print("Loop!", locked_cnt, key, seen[key], len(chamber))
                prev_locked_count, prev_chamber = seen[key]
                assert heights[prev_locked_count] == prev_chamber
                period = locked_cnt - prev_locked_count
                remaining = 1000000000000 - locked_cnt
                increase = (remaining // period) * (len(chamber) - prev_chamber)
                leftover = heights[prev_locked_count + remaining % period] - prev_chamber
                print(increase, leftover, remaining % period, period)
                print("Result: ", len(chamber) + increase + leftover)
                break
            else:
                seen[key] = (locked_cnt, len(chamber))
        i += 1
        i %= len(commands)
    print(len(chamber))
    # print('\n'.join(''.join(row) for row in chamber[::-1]))

def part2():
    print(len(read_input(17).strip()))

part1()