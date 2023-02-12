import os
import re

def read_input(day):
    with open("input%d.txt" % day, "rt") as f:
        return f.read().replace('\r', '')

def get_inp_lines(day):
    return [l.strip() for l in read_input(day).strip().split('\n')]

def part1():
    s = read_input(6).strip()
    i = 0
    while len(set(s[i:i+4])) < 4:
        i += 1
    print(i + 4)

def part2():
    s = read_input(6).strip()
    i = 0
    while len(set(s[i:i+14])) < 14:
        i += 1
    print(i + 14)

part2()