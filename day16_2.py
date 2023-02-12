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

def part2():
    name_to_node = {}
    def get_node(name):
        if name not in name_to_node:
            name_to_node[name] = Node(name)
        return name_to_node[name]

    for l in get_inp_lines(16):
        print(l)
        node, flow, ns = re.match('Valve (.*) has flow rate=(.*); tunnels? leads? to valves? (.*)', l).groups()
        node = get_node(node)
        node.flow = int(flow)
        node.ns = [get_node(n) for n in ns.split(', ')]

    all_pairs_paths = defaultdict(lambda x: float('inf'))
    for n in name_to_node.values():
        all_pairs_paths[(n, n)] = 0
        for n2 in n.ns:
            all_pairs_paths[(n, n2)] = 1

    progress = True
    while progress:
        progress = False
        for n1, n2, n3 in itertools.product(name_to_node.values(), repeat=3):
            l = all_pairs_paths[(n1, n2)] + all_pairs_paths[(n2, n3)]
            if l < all_pairs_paths[(n1, n3)]:
                all_pairs_paths[(n1, n3)] = l
                progress = True

    nodes = [n for n in name_to_node.values() if n.flow > 0]
    for i, n in enumerate(nodes):
        n.idx = i
    c = len(nodes)
    matrix = [all_pairs_paths[(nodes[i], nodes[j])] for i in range(c) for j in range(c)]
    flows = [n.flow for n in nodes]

    visited = set()
    open = [False] * c
    cache = {}
    def explore_from(node: int, ele: int, time_remaining: int):
        key = (min(node, ele), max(node, ele), time_remaining, tuple(open))
        if key in cache:
            return cache[key]
        if time_remaining <= 1:
            return 0
        #visited.add(node)
        best = 0
        for next_n in range(c):
            if not open[next_n]:
                continue
            open[next_n] = True
            for next_ele in range(c):
                if not open[next_ele]:
                    continue
                open[next_ele] = True
                    best = max(best, explore_from(next_n, next_ele, time_remaining - 1 - ))
                open[next_ele] = False
            open[next_n] = False
        result = best + (flows[node] + flows[ele]) * (time_remaining - 1)
        cache[key] = result
        return result

    print(explore_from(name_to_node['AA'].idx, name_to_node['AA'].idx, 26))

def part2_works():
    name_to_node = {}
    def get_node(name):
        if name not in name_to_node:
            name_to_node[name] = Node(name)
        return name_to_node[name]

    nodes = []
    for i, l in enumerate(get_inp_lines(16)):
        print(l)
        node, flow, ns = re.match('Valve (.*) has flow rate=(.*); tunnels? leads? to valves? (.*)', l).groups()
        node = get_node(node)
        node.flow = int(flow)
        node.ns = [get_node(n) for n in ns.split(', ')]
        if node.flow > 0:
            node.idx = len(nodes)
            nodes.append(node)
        node.idx2 = i

    open = [False] * len(nodes)
    cache = {}
    def explore_from(node: Node, time_remaining: int):
        #key = (2^16 * 30 * node.idx + 2^16 * time_remaining + sum(2**i if open[i] else 0 for i in range(len(open))))
        key = (2**16 * 30 * node.idx2 + 2**16 * time_remaining + sum(2**i if open[i] else 0 for i in range(len(open))))
        #key = (node.idx2, time_remaining, tuple(open))
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

    iter1 = itertools.product(*[[False, True] for n in nodes])
    iter2 = itertools.product(*[[True, False] for n in nodes])
    best = 0
    cnt = 0
    for op1, op2 in zip(iter1, iter2):
        open[:] = op1
        flow1 = explore_from(name_to_node['AA'], 26)
        open[:] = op2
        flow2 = explore_from(name_to_node['AA'], 26)
        best = max(best, flow1 + flow2)
        cnt += 1
        if cnt % 10 == 0:
            print(cnt)
    print(best)

def part2_works_compressed():
    name_to_node = {}
    def get_node(name):
        if name not in name_to_node:
            name_to_node[name] = Node(name)
        return name_to_node[name]

    nodes = []
    for i, l in enumerate(get_inp_lines(16)):
        print(l)
        node, flow, ns = re.match('Valve (.*) has flow rate=(.*); tunnels? leads? to valves? (.*)', l).groups()
        node = get_node(node)
        node.flow = int(flow)
        node.ns = [get_node(n) for n in ns.split(', ')]
        if node.flow > 0 or node.name == 'AA':
            node.idx = len(nodes)
            nodes.append(node)
            assert nodes[node.idx] is node
        node.idx2 = i


    all_pairs_paths = defaultdict(lambda: float('inf'))
    for n in name_to_node.values():
        all_pairs_paths[(n, n)] = 0
        for n2 in n.ns:
            all_pairs_paths[(n, n2)] = 1

    progress = True
    while progress:
        progress = False
        for n1, n2, n3 in itertools.product(name_to_node.values(), repeat=3):
            l = all_pairs_paths[(n1, n2)] + all_pairs_paths[(n2, n3)]
            if l < all_pairs_paths[(n1, n3)]:
                all_pairs_paths[(n1, n3)] = l
                progress = True

    c = len(nodes)
    matrix = [[all_pairs_paths[(nodes[i], nodes[j])] for i in range(c)] for j in range(c)]

    open = [False] * len(nodes)
    cache = {}
    def explore_from(node: Node, time_remaining: int):
        #key = (2^16 * 30 * node.idx + 2^16 * time_remaining + sum(2**i if open[i] else 0 for i in range(len(open))))
        # key = (2**16 * 30 * node.idx + 2**16 * time_remaining + sum(2**i if open[i] else 0 for i in range(len(open))))
        key = (node.idx, time_remaining, tuple(open))
        if key in cache:
            return cache[key]
        if time_remaining <= 1:
            return 0
        #visited.add(node)
        best = 0
        open[node.idx] = True
        for n in nodes:
            if open[n.idx]:
                continue
            t = time_remaining - matrix[n.idx][node.idx] - 1
            best = max(best, n.flow * t + explore_from(n, t))
        open[node.idx] = False
        #visited.remove(node)
        cache[key] = best
        return best

    # print(explore_from(name_to_node['AA'], 30))
    iter1 = itertools.product(*[[False, True] for n in nodes])
    iter2 = itertools.product(*[[True, False] for n in nodes])
    best = 0
    cnt = 0
    for op1, op2 in zip(iter1, iter2):
        open[:] = op1
        flow1 = explore_from(name_to_node['AA'], 26)
        open[:] = op2
        flow2 = explore_from(name_to_node['AA'], 26)
        best = max(best, flow1 + flow2)
        cnt += 1
        if cnt % 10 == 0:
            print(cnt)
    print(best)

part2()
        
