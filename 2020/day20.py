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


def prod(xs):
    acc = 1
    for x in xs:
        acc *= x
    return acc


def in_range(p, w):
    return 0 <= p[0] < w and 0 <= p[1] < w


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


def tile_transforms(tile):
    """Possible transformations of a block."""
    variants = []
    for k in range(0, 4):
        variants.append(np.rot90(tile, k=k))

    for v in variants:
        yield v

    for v in variants[:2]:
        yield np.flip(v, axis=0)
        yield np.flip(v, axis=1)


def tile_borders(tile):
    return tile[0], tile[-1], tile[:, 0], tile[:, -1]


def make_border(b):
    return np.array([ord(x) for x in b], dtype=np.int8)


def border_str(b):
    return ''.join(map(chr, b))


def other_tiles(tiles, current_id):
    for t_id, tile in tiles.items():
        if t_id == current_id:
            continue
        for t in tile_transforms(tile):
            yield t_id, t


def reconstruct(tiles):
    w = int(np.sqrt(len(tiles)))
    assert w * w == len(tiles), "not a square !"
    print(f"dimensions: {w}x{w}")

    tiles_transforms = {t_id: list(tile_transforms(x)) for t_id, x in
                        tiles.items()}
    tiles_borders = {t_id: [tile_borders(x) for x in cfg]
                     for t_id, cfg in tiles_transforms.items()}

    # def recons()
    pass
    return 42


def aoc_run(input_file):
    lines = list(open(input_file))
    tiles = parse(lines)
    tiles = {pid: np.array(x, dtype=np.int8) for pid, x in tiles.items()}
    m = reconstruct(tiles)

    n = part_1(tiles)
    print("part 1:", n)

    # ts = {pid: list(tile_transforms(x)) for pid, x in tiles.items()}
    # bs = {pid: [tile_borders(x) for x in cfg] for pid, cfg, in ts.items()}

    # print(draw(tiles[1171]))
    # print("")
    # reconstruct(parts, 1427)
    # return
    # for border in tile_borders(parts[1171]):
    #     print("border:", ''.join(map(chr, border)))
    # s = set(part_1(bs))
    # print(prod(s), s)
    # for pid, cfg_id, cfg in matching_tile(bs, make_border("...##....."), TOP):
    #     print("matching:", pid, cfg_id)
    #     print(draw(cfg))
    # part 1: 107399567124539

    # for pid, cfg in matching_borders()
    # print("\n====\n")
    # for d in transformed(parts[1171]):
    #     print(draw(d))
    #     print()


if __name__ == '__main__':
    aoc_run('assets/day20-input-1')
