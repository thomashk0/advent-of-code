# Skeleton for days
import collections
import copy
import itertools
from dataclasses import dataclass
from typing import Any

import aoc

DIRS = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}


def adjacent(x, dirs):
    for dx, dy in dirs:
        yield x[0] + dx, x[1] + dy


def tuple_add(p, q):
    return tuple(x + y for x, y in zip(p, q))


def tuple_mul(p, q):
    return tuple(x * y for x, y in zip(p, q))


def tuple_reverse(x):
    return tuple(reversed(x))


@dataclass
class Context:
    data: Any
    busy_cells: Any
    blizzards: Any
    shape: Any


def parse_input(raw: str):
    lines = raw.splitlines()
    blizzards = []
    data = {}
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c in ["<", ">", "v", "^"]:
                blizzards.append(((i, j), c))
                data[i, j] = "."
            else:
                data[i, j] = c
    return Context(
        data=data,
        busy_cells=set((i, j) for (i, j), _ in blizzards),
        blizzards=blizzards,
        shape=(len(lines), len(lines[0])),
    )


def update_blizzards(ctx: Context):
    busy = collections.defaultdict(int)
    new_blizzards = []
    for (i, j), d in ctx.blizzards:
        move_dir = DIRS[d]
        ni, nj = tuple_add((i, j), move_dir)
        # Wrapping rules...

        v = ctx.data.get((ni, nj), None)
        if v is None or v == "#":
            sh = tuple_mul(move_dir, (-(ctx.shape[0] + 1), -(ctx.shape[1] + 1)))
            start = tuple_add((ni, nj), sh)
            while ctx.data.get(start, None) != ".":
                start = tuple_add(start, move_dir)
            ni, nj = start
        busy[(ni, nj)] += 1
        new_blizzards.append(((ni, nj), d))
    ctx.blizzards = new_blizzards
    ctx.busy_cells = busy


def part_1(ctx: Context):
    ctx = copy.deepcopy(ctx)
    start = (0, 1)
    end = (ctx.shape[0] - 1, ctx.shape[1] - 2)
    assert ctx.data[start] == "."
    assert ctx.data[end] == "."

    found = move_to(ctx, end, start)
    return found


def move_to(ctx, target, src):
    locs = {src}
    found = None
    # my_loc = start
    for i in range(10000):
        update_blizzards(ctx)
        if target in locs:
            found = i
            break
        new_locs = set()
        for head in locs:
            for head_new in itertools.chain(adjacent(head, DIRS.values()), [head]):
                if head_new in ctx.busy_cells:
                    continue
                if ctx.data.get(head_new, None) != ".":
                    continue
                new_locs.add(head_new)
        locs = new_locs
    return found


def part_2(ctx):
    start = (0, 1)
    end = (ctx.shape[0] - 1, ctx.shape[1] - 2)
    assert ctx.data[start] == "."
    assert ctx.data[end] == "."
    found0 = move_to(ctx, end, start)
    found1 = move_to(ctx, start, end)
    found2 = move_to(ctx, end, start)
    return found0 + found1 + found2 + 2


def aoc_inputs():
    return {"example": ("day24-input-ex", 18, 54), "real": ("day24-input-1", 230, 713)}
