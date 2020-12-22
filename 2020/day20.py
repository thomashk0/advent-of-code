import collections
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
    yield px, py - 1
    yield px, py + 1
    yield px - 1, py
    yield px + 1, py


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


def tile_borders_str(tile):
    return tuple(map(border_str, tile_borders(tile)))


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


def border_info(borders):
    r = collections.defaultdict(list)
    for t_id, variants in borders.items():
        for v_id, bs in enumerate(variants):
            for b, d in zip(bs, ALL_DIRS):
                # b_str = border_str(b)
                r[b].append((t_id, v_id, d))
    return r


def draw_state(state, w):
    for row in range(w):
        for col in range(w):
            if x := state.get((row, col)):
                tid, vid = x
                print(f"{tid:4}.{vid:4}  ", end="")
            else:
                print("____.____  ", end="")
        print()


def reconstruct(tiles):
    w = int(np.sqrt(len(tiles)))
    assert w * w == len(tiles), "not a square !"
    print(f"dimensions: {w}x{w}")

    tiles_transforms = {t_id: list(tile_transforms(x)) for t_id, x in
                        tiles.items()}
    tiles_borders = {t_id: [tile_borders_str(x) for x in cfg]
                     for t_id, cfg in tiles_transforms.items()}
    info = border_info(tiles_borders)

    def borders_match(t_id, borders, dirs, values):
        for d, v in zip(dirs, values):
            b = borders[d]
            if v is None:
                if not all(id == t_id for id, _, _ in info[b]):
                    return False
            elif b != v:
                return False
        return True

    def blocs_matching(dirs, values):
        for t_id, variants in tiles_borders.items():
            for v_id, borders in enumerate(variants):
                if borders_match(t_id, borders, dirs, values):
                    yield t_id, v_id

    configs = []
    for t_id, v_id in blocs_matching([TOP, LEFT], (None, None)):
        configs.append({(0, 0): (t_id, v_id)})

    for i in range(500):
        current = configs[-1]
        reserved_ids = set(t for t, _ in current.values())
        remaining = set(
            x for p in current.keys() for x in adjacent(p)
            if in_range(x, w) and x not in current)
        if not remaining:
            # We can also yield to get all configs
            yield current

        print(f"=== round {i} (n_configs={len(configs)}) ===")
        draw_state(current, w)
        print()

        loc = next(iter(remaining))
        dirs = []
        values = []
        for dir, adj in zip(ALL_DIRS, adjacent(loc)):
            if not in_range(adj, w):
                dirs.append(dir)
                values.append(None)
            elif other := current.get(adj):
                o_tid, o_vid = other
                dirs.append(dir)
                values.append(tiles_borders[o_tid][o_vid][OPPOSITE[dir]])
        matching = list(blocs_matching(dirs, values))
        print(f"constraints: {loc}, {dirs}, {values} ==> {matching}")
        configs = configs[:-1]
        for m_tid, m_vid in matching:
            if m_tid in reserved_ids:
                continue
            cfg = copy.deepcopy(current)
            cfg[loc] = (m_tid, m_vid)
            configs.append(cfg)


def aoc_run(input_file):
    lines = list(open(input_file))
    tiles = parse(lines)
    tiles = {pid: np.array(x, dtype=np.int8) for pid, x in tiles.items()}
    w = int(np.sqrt(len(tiles)))
    solution = next(reconstruct(tiles))
    print(solution)
    corners = [(0, 0), (w - 1, 0), (0, w - 1), (w - 1, w - 1)]
    print("part 1:", prod([solution[c][0] for c in corners]))
    return


if __name__ == '__main__':
    aoc_run('assets/day20-input-1')
