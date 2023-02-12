import os
import re
from collections import defaultdict
from math import gcd
import functools
import numpy as np

def read_input(day):
    with open("input%s.txt" % day, "rt") as f:
        return f.read().replace('\r', '')

def get_inp_lines(day):
    return [l.strip() for l in read_input(day).strip().split('\n')]

RESOURCE_TYPES = ['ore', 'clay', 'obsidian', 'geode']

class Blueprint:
    def __init__(self, line):
        groups = re.match("Blueprint (.*): Each ore robot costs (.*) ore. Each clay robot costs (.*) ore. Each obsidian robot " +
            "costs (.*) ore and (.*) clay. Each geode robot costs (.*) ore and (.*) obsidian.", line).groups()
        groups = [int(d) for d in groups]
        self.name = groups[0]
        groups = groups[1:]
        self.costs = {
            'ore': {'ore': groups[0]},
            'clay': {'ore': groups[1]},
            'obsidian': {'ore': groups[2], 'clay': groups[3]},
            'geode': {'ore': groups[4], 'obsidian': groups[5]}
        }
        self.max_robots = [max(self.costs[r]['ore'] for r in ['clay', 'obsidian', 'geode'])]
        self.max_robots.append(self.costs['obsidian']['clay'])
        self.max_robots.append(self.costs['geode']['obsidian'])
        self.max_robots.append(1000)
        self.max_robots = np.array(self.max_robots)
        self.costs = [np.array([self.costs[k].get(k2, 0) for k2 in RESOURCE_TYPES], dtype=np.int32) for k in RESOURCE_TYPES]


NP_ZEROS = np.zeros([4], dtype=np.int32)

def is_feasible_new(blueprint: Blueprint, resources, robots, pending_robots):
    if np.any(robots + pending_robots > blueprint.max_robots):
        return False
    if np.sum(pending_robots) > 1:
        return False
    return True

def is_feasible_old(blueprint: Blueprint, resources, robots, pending_robots):
    # Prevent unneeded stockpiling.
    # if resources[1] > 30:
    #     return False
    non_zero_robots = robots + pending_robots > 0
    # State is feasible if there is a robot we are saving for that we can't afford and can get by waiting.
    for rob in range(4):
        if np.any(blueprint.costs[rob] > resources) and np.all(np.logical_or(np.equal(blueprint.costs[rob], 0), non_zero_robots)):
            return True
    return False

def step(blueprint: Blueprint, resources, robots, pending_robots, cache, results):
    key = tuple(pending_robots)
    if key in cache:
        return
    cache.add(key)
    for rob in range(4):
        # if rob < 3 and robots[rob + 1] > 0:
        #     continue
        if np.all(resources >= blueprint.costs[rob]):
            new_robots = pending_robots.copy()
            new_robots[rob] += 1
            step(blueprint, resources - blueprint.costs[rob], robots, new_robots, cache, results)
    if is_feasible_new(blueprint, resources, robots, pending_robots):
        new_resources = resources + robots
        for i in range(3):
            if robots[i] == blueprint.max_robots[i]:
                new_resources[i] = blueprint.max_robots[i]
        for i in range(3):
            if new_resources[i] > blueprint.max_robots[i] * 2:
                new_resources[i] = blueprint.max_robots[i] * 2
        results.append((new_resources, robots + pending_robots))

class HierarchicalLookup:
    def __init__(self, i, data):
        self.depth = i
        self.max = np.max(data, axis=0, keepdims=False)
        if i == 8:
            self.data = data
        else:
            self.data = None
            bins = defaultdict(list)
            for d in data:
                bins[d[i]].append(d)
            self.children = {k: HierarchicalLookup(i + 1, bin) for k, bin in bins.items()}
    
    def lookup(self, data, strict):
        if self.depth == 8:
            return not strict
        if not np.all(data <= self.max):
            return False
        child = self.children.get(data[self.depth])
        if child is not None and child.lookup(data, strict):
            return True
        return any(c.lookup(data, strict=False) for k, c in self.children.items() if k > data[self.depth])

    def __repr__(self):
        if self.depth == 8:
            return repr(self.data)
        return ', '.join('%s: %s' % (k, len(self.children[k])) for k in sorted(self.children.keys()))

def compress(states):
    def get_key(state):
        return tuple([c for t in zip(state[1], state[0]) for c in t])
    keys = [get_key(state) for state in states]
    arrays = [np.array(k) for k in keys]
    result_states = []
    used_keys = set()
    lookup = HierarchicalLookup(0, arrays)
    for s, k, arr in zip(states, keys, arrays):
        if k not in used_keys:
            used_keys.add(k)
            if not lookup.lookup(arr, strict=True):
                result_states.append(s)
    return result_states


def compress_old(states):
    new_states = []
    for i, state1 in enumerate(states):
        for j, state2 in enumerate(states):
            if np.all(state2[0] >= state1[0]) and np.all(state2[1] >= state1[1]):
                if np.any(state2[0] > state1[0]) or np.any(state2[1] > state1[1]) or j > i:
                    break
        else:
            new_states.append(state1)
    return new_states

def num_geodes(blueprint: Blueprint, time_remaining, resources, robots, pending_robots, cache):
    key = (time_remaining, tuple(resources), tuple(robots), tuple(pending_robots))
    if key in cache:
        return cache[key]
    if time_remaining == 0:
        return resources[2]
    best = 0
    for rob in range(4):
        if np.all(resources >= blueprint.costs[rob]):
            new_robots = pending_robots.copy()
            new_robots[rob] += 1
            best = max(best, num_geodes(blueprint, time_remaining, resources - blueprint.costs[rob], robots, new_robots, cache))
    
    best = max(best, num_geodes(blueprint, time_remaining - 1, resources + robots, robots + pending_robots, NP_ZEROS, cache))
    
    cache[key] = best
    return best

def part1():
    blueprints = [Blueprint(l) for l in get_inp_lines('19')]
    for blueprint in blueprints[:3]:
        state = [(NP_ZEROS, np.array([1, 0, 0, 0], dtype=np.int32))]
        for i in range(32):
            next_states = []
            for resources, robotos in state:
                cache = set()
                step(blueprint, resources, robotos, NP_ZEROS, cache, next_states)
            print(len(next_states))
            state = compress(next_states)
            # state_backup = compress_old(next_states)
            if i == 24:
                import random
                for s in random.choices(state, k=20):
                    print(s)
            print(i, len(next_states), len(state))
        print("BLUEPRINT %s RESULTS!" % blueprint.name)
        print(len(state))
        print(max(s[0][3] for s in state))

    # cache = {}
    # test = num_geodes(blueprints[0], 13, NP_ZEROS, np.array([1, 0, 0, 0], dtype=np.int32), NP_ZEROS, cache)
    # print(len(cache))
    # keys = list(k for k in cache.keys() if k[0] == 5 and k[3] == (0, 0, 0, 0))
    # print(len(keys))
    # import random
    # for c in random.choices(keys, k=20):
    #     print(c)
    # print(test)

def main():
    result = [(1, 3),
        (2, 13),
        (3, 0),
        (4, 0),
        (5, 0),
        (6, 10),
        (7, 0),
        (8, 7),
        (9, 0),
        (10, 2),
        (11, 0),
        (12, 0),
        (13, 1),
        (14, 12),
        (15, 1),
        (16, 0),
        (17, 0),
        (18, 0),
        (19, 0),
        (20, 0),
        (21, 7),
        (22, 1),
        (23, 0),
        (24, 15),
        (25, 1),
        (26, 3),
        (27, 8),
        (28, 1),
        (29, 1),
        (30, 3)]
    print(sum(x*y for x,y in result))

part1()