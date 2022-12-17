import re

from tqdm import tqdm, trange

from aoc import SparseMap

COORDS_RE = re.compile(r"x=(-?\d+), y=(-?\d+)")


def limits(d):
    xs = [x for x, _ in d.keys()]
    ys = [y for _, y in d.keys()]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    return (xmin, xmax), (ymin, ymax)


def dist(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def parse_input(raw: str):
    sensors = set()
    beacons = set()
    closest = {}
    for line in raw.splitlines():
        sensor, beacon = COORDS_RE.findall(line)
        sensor, beacon = tuple(map(int, sensor)), tuple(map(int, beacon))
        closest[sensor] = (dist(sensor, beacon), beacon)
        sensors.add(sensor)
        beacons.add(beacon)
    return sensors, beacons, closest


# DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def around(p):
    px, py = p
    yield px + 1, py
    yield px - 1, py
    yield px, py + 1
    yield px, py - 1


def around_y(p):
    px, py = p
    yield px + 1, py
    yield px - 1, py


def expand(carto, start, dist):
    to_explore = {start}
    explored = set()
    for i in range(dist + 1):
        to_explore_next = set()
        for n in to_explore:
            explored.add(n)
            if n not in carto.data:
                carto[n] = "#"
            for n_next in around(n):
                if n_next not in explored:
                    to_explore_next.add(n_next)
        to_explore = to_explore_next


def expand_along_y(carto, start, d_max, y):
    # This is the closest point on the line y:
    r_start = (start[0], y)

    if dist(r_start, start) > d_max:
        # No need to search: we are already to far
        return
    to_explore = {r_start}
    explored = set()
    while len(to_explore) > 0:
        to_explore_next = set()
        for n in to_explore:
            explored.add(n)
            if n not in carto.data:
                carto[n] = "#"
            for n_next in around_y(n):
                if n_next not in explored and dist(n_next, start) <= d_max:
                    to_explore_next.add(n_next)
        to_explore = to_explore_next
    pass


def part_1(input):
    sensors, beacons, closest = input
    merged = dict((k, "S") for k in sensors)
    merged.update((k, "B") for k in beacons)

    if len(sensors) == 14:
        target_line = 10
    else:
        target_line = 2000000

    carto = SparseMap(merged, ".")
    for s in sensors:
        expand_along_y(carto, s, closest[s][0], target_line)
    dst = sum(v == "#" for k, v in carto.data.items() if k[1] == target_line)
    return dst


def symb_abs(x):
    from z3 import If

    return If(x >= 0, x, -x)


def part_2(input):
    if len(input) == 14:
        return None

    sensors, beacons, closest = input
    from z3 import Solver, Int

    limit = 4000000
    solver = Solver()
    x = Int("x")
    y = Int("y")
    solver.add(x >= 0, x <= limit)
    solver.add(y >= 0, y <= limit)
    for s in sensors:
        solver.add(symb_abs(x - s[0]) + symb_abs(y - s[1]) > closest[s][0])
    solver.check()
    m = solver.model()
    return m[x].as_long() * 4000000 + m[y].as_long()


def aoc_inputs():
    return {
        # "example": ("day15-input-ex", 26, 56000011),
        "real": ("day15-input-1", 6275922, 11747175442119)
    }
