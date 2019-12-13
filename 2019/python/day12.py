import copy
import itertools
import math
import re

LINE_RE = re.compile("<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")


def sign(x):
    if x == 0:
        return 0
    return 1 if x >= 0 else -1


def parse(f):
    for l in f:
        yield tuple(map(int, LINE_RE.match(l.strip()).groups()))


def load_file(f_name):
    with open(f_name) as f:
        return [[x, y, z, 0, 0, 0] for x, y, z in parse(f)]


def apply_gravity(coords):
    for p, q in itertools.combinations(coords, 2):
        for i in range(3):
            p[3 + i] += sign(q[i] - p[i])
            q[3 + i] += sign(p[i] - q[i])
        assert p != q


def update_positions(coords):
    for p in coords:
        for i in range(3):
            p[i] += p[i + 3]


def moon_energy(moon):
    return sum(map(abs, moon[:3])) * sum(map(abs, moon[3:]))


def dump(coords):
    for p in coords:
        px, py, pz, vx, vy, vz = tuple(p)
        print(
            f"pos=<x={px:2}, y={py:3}, z={pz:2}>, vel=<x={vx:2}, y={vy:2}, z={vz:2}>")


def step(coords):
    apply_gravity(coords)
    update_positions(coords)


def part_1(coords, steps):
    for i in range(steps):
        step(coords)
    return sum(map(moon_energy, coords))


def state(coords):
    return tuple(map(tuple, coords))


def partial_state(coords, i):
    return tuple((p[i], p[i + 3]) for p in coords)


def repeat_along(coords, axis):
    old_states = set()
    i = 0
    while True:
        s = partial_state(coords, axis)
        if s in old_states:
            return i
        old_states.add(s)
        i += 1
        step(coords)


def part_2_naive(coords):
    old_states = set()
    i = 0
    while True:
        s = state(coords)
        if s in old_states:
            return i
        old_states.add(s)
        i += 1
        step(coords)


def lcm(x, y):
    return (x * y) // math.gcd(x, y)


def part_2(coords, debug=False):
    xs = []
    for i in range(3):
        n = repeat_along(copy.copy(coords), i)
        if debug:
            print(f"axis={i}, repeat after {n} steps")
        xs.append(n)
    acc = xs[0]
    for x in xs[1:]:
        acc = lcm(acc, x)
    return acc


def main():
    assert part_1(load_file("assets/day12-example-0"), 10) == 179
    assert part_1(load_file("assets/day12-example-1"), 100) == 1940
    print("part 1:", part_1(load_file("assets/day12-input"), 1000))

    assert part_2_naive(load_file("assets/day12-example-0")) == 2772
    assert part_2(load_file("assets/day12-example-0")) == 2772
    print("part 2:", part_2(load_file('assets/day12-input')))

if __name__ == '__main__':
    main()
