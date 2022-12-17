# Skeleton for days
import copy
import re

from aoc import SparseMap

COORDS_RE = re.compile(r"(\d+),(\d+)")


def parse_input(raw: str):
    paths = []
    for line in raw.splitlines():
        path = [(int(x[0]), int(x[1])) for x in COORDS_RE.findall(line)]
        paths.append(path)
    sparse_map = {}
    for p in paths:
        for (x, y), (x_old, y_old) in zip(p[1:], p):
            dx = max(min(x - x_old, 1), -1)
            dy = max(min(y - y_old, 1), -1)
            sparse_map[(x, y)] = "#"
            while x_old != x or y_old != y:
                sparse_map[(x_old, y_old)] = "#"
                x_old += dx
                y_old += dy
    return SparseMap(sparse_map, ".")


DIRS = [(0, 1), (-1, 1), (1, 1)]


def spawn_sand(input) -> bool:
    _, (_, y_max) = input.limits()
    cx, cy = (500, 0)

    while True:
        new_loc = None
        for dx, dy in DIRS:
            t = (cx + dx, cy + dy)
            if t not in input.data:
                new_loc = t
                break
        if new_loc is None:
            input.data[cx, cy] = "O"
            return False
        elif new_loc[1] > y_max:
            return True
        cx, cy = new_loc


def part_1(input: SparseMap):
    input = copy.deepcopy(input)
    i = 0
    while True:
        done = spawn_sand(input)
        if done:
            return i
        i += 1


def spawn_sand_2(input, y_max):
    cx, cy = (500, 0)
    while True:
        new_loc = None
        for dx, dy in DIRS:
            t = (cx + dx, cy + dy)
            if t not in input.data:
                new_loc = t
                break
        if new_loc is None:
            input.data[cx, cy] = "O"
            return
        elif new_loc[1] == y_max + 2:
            input.data[cx, cy] = "O"
            return
        cx, cy = new_loc


def part_2(input):
    i = 0
    _, (_, y_max) = input.limits()
    while True:
        if input.data.get((500, 0)) == "O":
            return i
        spawn_sand_2(input, y_max)
        i += 1


def aoc_inputs():
    return {
        "example": ("day14-input-ex", 24, 93),
        "real": ("day14-input-1", None, None),
    }
