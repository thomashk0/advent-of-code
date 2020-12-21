import copy
import re
import numpy as np

TILE_RE = re.compile("Tile (\d+):")

TOP, BOT, LEFT, RIGHT = 0, 1, 2, 3
ALL_DIRS = [0, 1, 2, 3]
OPPOSITE = [1, 0, 3, 2]
DIR_M = {
    (1, 0): LEFT,
    (-1, 0): RIGHT,
    (0, 1): BOT,
    (0, -1): TOP
}


def adjacent(p):
    px, py = p
    yield px + 1, py
    yield px - 1, py
    yield px, py + 1
    yield px, py - 1


def diff(pa, pb):
    return pb[0] - pa[0], pb[1] - pa[1]


def get_dir(pa, pb):
    return DIR_M[diff(pa, pb)]


def parse_map(lines):
    m = []
    for i, line in enumerate(lines):
        if not line.strip():
            return m, lines[i + 1:]
        row = []
        for char in line.strip():
            row.append(ord(char))
        m.append(row)
    return m, []


def parse(lines):
    parts = {}
    while lines:
        l = lines[0]
        part_id = int(TILE_RE.match(l).group(1))
        m, lines = parse_map(lines[1:])
        parts[part_id] = m
    return parts


def draw(x):
    return "\n".join(''.join(map(chr, row)) for row in x)


def transformed(tile):
    variants = []
    for k in range(0, 4):
        variants.append(np.rot90(tile, k=k))

    for v in variants:
        yield v
    for v in variants[:2]:
        yield np.flip(v, axis=0)
        yield np.flip(v, axis=1)
        # This one is redundant?
        # yield np.flip(np.flip(v, axis=1), axis=0)


def tile_borders(tile):
    return tile[0], tile[-1], tile[:, 0], tile[:, -1]


def make_border(b):
    return np.array([ord(x) for x in b], dtype=np.int8)


def border_str(b):
    return ''.join(map(chr, b))


def matching_tile(bs, border, dir):
    dir_n = OPPOSITE[dir]
    for pid, variants in bs.items():
        for cfg_id, cfg in enumerate(variants):
            if np.all(border == cfg[dir_n]):
                yield pid, cfg_id, cfg


def reconstruct(tiles, first_bloc):
    unplaced = set(tiles.keys())
    unplaced.remove(first_bloc)
    final_map = {(0, 0): tiles[first_bloc]}
    empty_locations = set(adjacent((0, 0)))

    def can_fit(b, loc):
        for p in adjacent(loc):
            other = final_map.get(p)
            if other is not None:
                dir = get_dir(loc, p)
                dir_n = OPPOSITE[dir]
                if np.any(tile_borders(b)[dir] != tile_borders(other)[dir_n]):
                    return False
        return True

    while True:
        if not unplaced:
            return final_map

        found = False
        for p in empty_locations:
            # print("analysis", p, empty_locations)
            choices = []
            for b_id in unplaced:
                for variant in transformed(tiles[b_id]):
                    if can_fit(variant, p):
                        choices.append((b_id, variant))
            if len(choices) == 1:
                b_id, b = choices[0]
                print("placing block:", p, b_id)
                unplaced.remove(b_id)
                empty_locations.remove(p)
                for adj in adjacent(p):
                    if adj not in final_map:
                        empty_locations.add(adj)
                found = True
                break
            print("alternatives:", len(choices))
        if not found:
            raise ValueError("iteration without effect...")


def part_1(bs, dirs=[BOT, RIGHT]):
    for pid, variants in bs.items():
        for cfg in variants:
            tot = 0
            for d in dirs:
                n_matching = sum(o_pid != pid for o_pid, _, _ in
                                 matching_tile(bs, cfg[d], d))
                if n_matching == 0:
                    tot += 1
            if tot == len(dirs):
                print(pid)
                yield pid


def prod(xs):
    acc = 1
    for x in xs:
        acc *= x
    return acc


def aoc_run(input_file):
    lines = list(open(input_file))
    parts = parse(lines)
    parts = {pid: np.array(x, dtype=np.int8) for pid, x in parts.items()}
    ts = {pid: list(transformed(x)) for pid, x in parts.items()}
    bs = {pid: [tile_borders(x) for x in cfg] for pid, cfg, in ts.items()}


    print(draw(parts[1171]))
    print("")
    reconstruct(parts, 1427)
    return
    for border in tile_borders(parts[1171]):
        print("border:", ''.join(map(chr, border)))
    s = set(part_1(bs))
    print(prod(s), s)
    for pid, cfg_id, cfg in matching_tile(bs, make_border("...##....."), TOP):
        print("matching:", pid, cfg_id)
        print(draw(cfg))
    # part 1: 107399567124539

    # for pid, cfg in matching_borders()
    # print("\n====\n")
    # for d in transformed(parts[1171]):
    #     print(draw(d))
    #     print()


if __name__ == '__main__':
    aoc_run('assets/day20-example-1')
