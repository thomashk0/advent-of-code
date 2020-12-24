import re

from utils import lmap

DIRS = {
    'e': (4, 0),
    'w': (-4, 0),
    'ne': (2, 3),
    'se': (2, -3),
    'nw': (-2, 3),
    'sw': (-2, -3)
}

TILE_RE = re.compile(r'e|w|ne|se|nw|sw')


def p2_add(p, q):
    return p[0] + q[0], p[1] + q[1]


def adjacent(p):
    for d in DIRS.values():
        yield p2_add(p, d)


def parse(lines):
    for line in lines:
        yield lmap(lambda x: DIRS[x], TILE_RE.findall(line))


def move(path, start=(0, 0)):
    for vec in path:
        start = p2_add(start, vec)
    return start


def constant_factory(value):
    return lambda: value


def step(black_tiles):
    to_explore = set(black_tiles)
    for p in black_tiles:
        to_explore.update(adjacent(p))
    new = set()
    for p in to_explore:
        n_black = sum(pa in black_tiles for pa in adjacent(p))
        if p not in black_tiles and n_black == 2:
            new.add(p)
        else:
            # black tile
            if p in black_tiles and not (n_black == 0 or n_black > 2):
                new.add(p)
    return new


def part_2(black_tiles):
    for i in range(100):
        black_tiles = step(black_tiles)
        # print(f"Day {i + 1}: {len(black_tiles)}")
    return black_tiles


def aoc_run(input_path):
    import collections
    tile_paths = list(parse(open(input_path)))

    d = collections.defaultdict(constant_factory(1))
    for p in tile_paths:
        dst = move(p)
        d[dst] ^= 1

    black_tiles = set(k for k, v in d.items() if v == 0)
    print("part 1:", len(black_tiles))
    print("part 2:", len(part_2(black_tiles)))


if __name__ == '__main__':
    aoc_run('assets/day24-input-1')
