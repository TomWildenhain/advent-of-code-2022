import os
import re
from collections import defaultdict

def read_input(day):
    with open("input%d.txt" % day, "rt") as f:
        return f.read().replace('\r', '')

def get_inp_lines(day):
    return [l.strip() for l in read_input(day).strip().split('\n')]

def read_grid():
    return [[int(c) for c in l] for l in get_inp_lines(8)]

def prod(l):
    res = 1
    for x in l:
        res *= x
    return res

def part1():
    g = read_grid()
    h = len(g)
    w = len(g[0])
    cnt = 0
    for x in range(w):
        for y in range(h):
            left = g[y][:x]
            right = g[y][x+1:]
            above = [l[x] for l in g[:y]]
            below = [l[x] for l in g[y+1:]]
            visible = any(all(g[y][x] > d for d in around) for around in [left, right, above, below])
            cnt += int(visible)
    print(cnt)

def part2():
    g = read_grid()
    h = len(g)
    w = len(g[0])
    sscores = []
    for x in range(w):
        for y in range(h):
            left = (g[y][:x])[::-1]
            right = g[y][x+1:]
            above = [l[x] for l in g[:y]][::-1]
            below = [l[x] for l in g[y+1:]]
            scores = []
            height = g[y][x]
            for around in [left, right, above, below]:
                r = 0
                for t in around:
                    r += 1
                    if t >= height:
                        break
                scores.append(r)
            #print(scores)
            sscores.append(prod(scores))
    print(max(sscores))

part2()