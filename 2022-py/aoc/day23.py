import collections
import itertools

from aoc import SparseMap


def parse_input(raw: str):
    m = {}
    for i, line in enumerate(raw.splitlines()):
        for j, c in enumerate(line):
            if c == '#':
                m[i, j] = '#'
    return m


# DIRS_8 = [(i, j) for i, j in itertools.product(range(-1, 2), range(-1, 2)) if not (i == 0 and j == 0)]
# DIRS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

DIRS = {
    "N": (-1, 0),
    "NE": (-1, 1),
    "NW": (-1, -1),
    "S": (1, 0),
    "SE": (1, 1),
    "SW": (1, -1),
    "E": (0, 1),
    "W": (0, -1)
}


def adjacent(x, dirs):
    for dx, dy in dirs:
        yield x[0] + dx, x[1] + dy


def is_alone(m, x, dirs):
    for adj in adjacent(x, dirs):
        if adj in m:
            return False
    return True


def tuple_add(p, q):
    return tuple(x + y for x, y in zip(p, q))


def part_1(args):
    choices = [
        (DIRS["N"], DIRS["NE"], DIRS["NW"]),
        (DIRS["S"], DIRS["SE"], DIRS["SW"]),
        (DIRS["W"], DIRS["NW"], DIRS["SW"]),
        (DIRS["E"], DIRS["NE"], DIRS["SE"]),
    ]
    m = set(args.keys())
    for i in range(10):
        m_new = update_round(m, choices)
        choices = choices[1:] + [choices[0]]
        m = m_new
    d = SparseMap({(k[1], k[0]): "#" for k in m}, default=".")
    (x_min, x_max), (y_min, y_max) = d.limits()
    w = x_max - x_min + 1
    h = y_max - y_min + 1
    return w * h - len(m)


def update_round(m, choices):
    moves = []
    occupied = collections.defaultdict(int)
    m_new = set()
    for elf in m:
        if is_alone(m, elf, DIRS.values()):
            m_new.add(elf)
            occupied[elf] += 1
            continue
        found = False
        for proposed_dir in choices:
            if is_alone(m, elf, proposed_dir):
                moves.append((elf, proposed_dir[0]))
                found = True
                break
        if not found:
            m_new.add(elf)
            occupied[elf] += 1

    actual_moves = 0
    for elf, new_dir in moves:
        occupied[tuple_add(elf, new_dir)] += 1
    for elf, new_dir in moves:
        p = tuple_add(elf, new_dir)
        if occupied[p] > 1:
            m_new.add(elf)
        else:
            assert p not in m_new
            actual_moves += 1
            m_new.add(p)
    if actual_moves == 0:
        return None
    assert len(m_new) == len(m)
    return m_new


def part_2(args):
    choices = [
        (DIRS["N"], DIRS["NE"], DIRS["NW"]),
        (DIRS["S"], DIRS["SE"], DIRS["SW"]),
        (DIRS["W"], DIRS["NW"], DIRS["SW"]),
        (DIRS["E"], DIRS["NE"], DIRS["SE"]),
    ]
    m = set(args.keys())
    round = 0
    while True:
        m_new = update_round(m, choices)
        if m_new is None:
            return round + 1
        m = m_new
        choices = choices[1:] + [choices[0]]
        round += 1


def aoc_inputs():
    return {
        "example": ("day23-input-ex-2", 110, 20),
        "real": ("day23-input-1", 4254, 992)
    }
