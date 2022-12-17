# Skeleton for days
import itertools
import pprint
import re
import time

import networkx as nx

from networkx import DiGraph

INPUT_RE = re.compile(r"Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? (.*)")


def parse_input(raw: str):
    g = DiGraph()
    for line in raw.splitlines():
        src, flow, dst = INPUT_RE.match(line).groups()
        for d in dst.split(", "):
            g.add_edge(src, d)
        g.nodes[src]["flow"] = int(flow)
    return g


def bit_is_set(x, n):
    return (x >> n) & 1


def set_bit(x, n):
    return x | (1 << n)


def clear_bit(x, n):
    return x & (0xFFFF_FFFF_FFFF_FFFF ^ (1 << n))


def memo_solve_p1(cache, valves, dists, start, opened, clock):
    key = start, opened, clock
    v = cache.get(key)
    if v is not None:
        return cache[key]
    r = solve_p1(cache, valves, dists, start, opened, clock)
    cache[key] = r
    return r


def solve_p1(cache, flow, dists, start, opened, clock):
    if clock <= 0:
        return 0, opened
    best = 0, opened
    opened_new = set_bit(opened, start)
    for i in range(len(flow)):
        if i == start:
            continue
        if not bit_is_set(opened_new, i):
            x = memo_solve_p1(cache, flow, dists, i, opened_new, clock - 1 - dists[start, i])
            if x[0] > best[0]:
                best = x
    return clock * flow[start] + best[0], set_bit(best[1], start)


def part_1(input: DiGraph):
    import numpy as np
    distances = nx.floyd_warshall(input)
    valves = [("AA", 0)] + [(n, input.nodes[n]["flow"]) for n in input.nodes if input.nodes[n]["flow"] > 0]
    valves_flow = [v[1] for v in valves]
    valve_distances = np.array([[distances[i][j] for j, _ in valves] for i, _ in valves], dtype=np.int64)
    cache = {}
    r = memo_solve_p1(cache, valves_flow, valve_distances, 0, 0, 30)
    return r[0]


def part_2(input: DiGraph):
    return None


def aoc_inputs():
    return {
        "example": ("day16-input-ex", 1651, 1707),
        # "example-2": ("day16-input-2", None, None),
        "real": ("day16-input-1", 2077, None)
    }
