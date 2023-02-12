import os
import re
from collections import defaultdict

def read_input(day):
    with open("input%d.txt" % day, "rt") as f:
        return f.read().replace('\r', '')

def get_inp_lines(day):
    return [l.strip() for l in read_input(day).strip().split('\n')]

def part1():
    lines = get_inp_lines(9)
    head = [0, 0]
    tail = [0, 0]
    directions = {
        'U': (0, -1),
        'D': (0, 1),
        'L': (-1, 0),
        'R': (1, 0)
    }
    locs = set()
    def do_move(vect):
        head[0] += vect[0]
        head[1] += vect[1]
        if abs(head[0] - tail[0]) == 2:
            tail[1] = head[1]
            tail[0] = (head[0] + tail[0]) // 2
        if abs(head[1] - tail[1]) == 2:
            tail[0] = head[0]
            tail[1] = (head[1] + tail[1]) // 2
        locs.add(tuple(tail))

    for l in lines:
        d, x = l.split(' ')
        x = int(x)
        vect = directions[d]
        for i in range(x):
            do_move(vect)

    print(len(locs))

def part2():
    lines = get_inp_lines(9)
    knots = [[0, 0] for _ in range(10)]
    directions = {
        'U': (0, -1),
        'D': (0, 1),
        'L': (-1, 0),
        'R': (1, 0)
    }
    locs = set()
    def do_move(vect):
        head = knots[0]
        head[0] += vect[0]
        head[1] += vect[1]

        for i in range(len(knots) - 1):
            knot1 = knots[i]
            knot2 = knots[i + 1]
            if abs(knot1[0] - knot2[0]) >= 2 and abs(knot1[1] - knot2[1]) >= 2:
                knot2[1] = (knot1[1] + knot2[1]) // 2
                knot2[0] = (knot1[0] + knot2[0]) // 2
            elif abs(knot1[0] - knot2[0]) == 2:
                knot2[1] = knot1[1]
                knot2[0] = (knot1[0] + knot2[0]) // 2
            elif abs(knot1[1] - knot2[1]) == 2:
                knot2[0] = knot1[0]
                knot2[1] = (knot1[1] + knot2[1]) // 2
        locs.add(tuple(knots[-1]))

    for l in lines:
        d, x = l.split(' ')
        x = int(x)
        vect = directions[d]
        for i in range(x):
            do_move(vect)

    print(len(locs))


part2()