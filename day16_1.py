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

class Node:
    def __init__(self, name, flow=0, ns=None):
        self.name = name
        self.flow = flow
        self.ns = ns or []
        self.idx = 0

    def __repr__(self) -> str:
        return 'Node(%s, %d, %s)' % (self.name, self.flow, ','.join(n.name for n in self.ns))

def part1():
    name_to_node = {}
    def get_node(name):
        if name not in name_to_node:
            name_to_node[name] = Node(name)
        return name_to_node[name]

    for i, l in enumerate(get_inp_lines(16)):
        print(l)
        node, flow, ns = re.match('Valve (.*) has flow rate=(.*); tunnels? leads? to valves? (.*)', l).groups()
        node = get_node(node)
        node.flow = int(flow)
        node.ns = [get_node(n) for n in ns.split(', ')]
        node.idx = i

    visited = set()
    open = [False] * len(name_to_node)
    cache = {}
    def explore_from(node: Node, time_remaining: int):
        key = (node, time_remaining, tuple(open))
        if key in cache:
            return cache[key]
        if time_remaining <= 1:
            return 0
        #visited.add(node)
        best = 0
        for n in node.ns:
            best = max(best, explore_from(n, time_remaining - 1))

        if node.flow != 0 and not open[node.idx]:
            open[node.idx] = True
            best = max(best, node.flow * (time_remaining - 1) + explore_from(node, time_remaining - 1))
            open[node.idx] = False
        #visited.remove(node)
        cache[key] = best
        return best

    print(explore_from(name_to_node['AA'], 30))
    print(len(cache))

def part2():
    name_to_node = {}
    def get_node(name):
        if name not in name_to_node:
            name_to_node[name] = Node(name)
        return name_to_node[name]

    for i, l in enumerate(get_inp_lines(16)):
        print(l)
        node, flow, ns = re.match('Valve (.*) has flow rate=(.*); tunnels? leads? to valves? (.*)', l).groups()
        node = get_node(node)
        node.flow = int(flow)
        node.ns = [get_node(n) for n in ns.split(', ')]
        node.idx = i

    visited1 = [False] * len(name_to_node)
    visited2 = [False] * len(name_to_node)
    open = [False] * len(name_to_node)
    cache1 = defaultdict(list)
    cache = {}

    best_ever = [0]
    def explore_from(node: Node, ele: Node, time_remaining: int, score, blocked_n=None, blocked_e=None):
        key1 = (min(id(node), id(ele)), max(id(ele), id(node)), tuple(open))
        key2 = (key1, time_remaining)
        if key2 in cache:
            return score + cache[key2]
        best_possible = sum(n.flow for n in name_to_node.values()) * (time_remaining - 1)
        if best_possible + score <= best_ever[0]:
            return 0
        if key1 in cache1:
            for time, prev_score in cache1[key1]:
                if time > time_remaining and prev_score <= best_ever[0] - score:
                    return 0
            
        if time_remaining <= 1:
            best_ever[0] = max(best_ever[0], score)
            return score
        if visited1[node.idx] or visited2[ele.idx]:
            return 0
        # visited1[node.idx] = True
        # visited2[ele.idx] = True
        best = 0
        def options(n, blocked):
            for next_n in n.ns:
                if next_n is blocked:
                    continue
                yield (next_n, 0, n)
            if n.flow != 0 and not open[n.idx]:
                open[n.idx] = True
                yield (n, n.flow * (time_remaining - 1), None)
                open[n.idx] = False
        for next_n, points1, next_blocked_n in options(node, blocked_n):
            for next_ele, points2, next_blocked_e in options(ele, blocked_e):
                best = max(best, explore_from(next_n, next_ele, time_remaining - 1, score + points1 + points2, next_blocked_n, next_blocked_e))

        #visited.remove(node)
        cache[key2] = best - score
        cache1[key1].append((time_remaining, best - score))
        # visited1[node.idx] = False
        # visited2[ele.idx] = False
        return best

    print(explore_from(name_to_node['AA'], name_to_node['AA'], 13, 0))
    print(len(cache))
    print(len(cache1))

part1()
        
