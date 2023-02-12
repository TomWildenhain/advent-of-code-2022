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
        self.blueprint = groups[0]
        groups = groups[1:]
        self.costs = {
            'ore': {'ore': groups[0]},
            'clay': {'ore': groups[1]},
            'obsidian': {'ore': groups[2], 'clay': groups[3]},
            'geode': {'ore': groups[4], 'obsidian': groups[5]}
        }
        self.costs = [np.array([self.costs[k].get(k2, 0) for k2 in RESOURCE_TYPES], dtype=np.int32) for k in RESOURCE_TYPES]

NP_ZEROS = np.zeros([4], dtype=np.int32)

def step(blueprint: Blueprint, resources, robots, pending_robots, cache, results):
    key = tuple(pending_robots)
    if key in cache:
        return
    cache.add(key)
    for rob in range(4):
        if np.all(resources >= blueprint.costs[rob]):
            new_robots = pending_robots.copy()
            new_robots[rob] += 1
            step(blueprint, resources - blueprint.costs[rob], robots, new_robots, cache, results)
    results.append((resources + robots, robots + pending_robots))

def compress(states):
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
    blueprints = [Blueprint(l) for l in get_inp_lines('19_test')]

    state = [(NP_ZEROS, np.array([1, 0, 0, 0], dtype=np.int32))]
    for i in range(18):
        next_states = []
        for resources, robotos in state:
            cache = set()
            step(blueprints[0], resources, robotos, NP_ZEROS, cache, next_states)
        print(len(next_states))
        state = compress(next_states)
        print(i, len(next_states), len(state))
    print(len(state))

    # cache = {}
    # test = num_geodes(blueprints[0], 13, NP_ZEROS, np.array([1, 0, 0, 0], dtype=np.int32), NP_ZEROS, cache)
    # print(len(cache))
    # keys = list(k for k in cache.keys() if k[0] == 5 and k[3] == (0, 0, 0, 0))
    # print(len(keys))
    # import random
    # for c in random.choices(keys, k=20):
    #     print(c)
    # print(test)


part1()