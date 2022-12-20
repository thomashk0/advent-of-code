import numpy as np
from tqdm import trange


def parse_input(raw: str):
    return [int(x) for x in raw.splitlines()]


def dump_seq(seq, loc):
    loc_rel = [(v, l % len(seq), i) for v, (l, i) in zip(seq, loc)]
    loc_rel.sort(key=lambda x: (x[1], x[2]))
    return loc_rel


def flatten_list(d, start, direction=2):
    cursor = start
    r = []
    for i in range(len(d)):
        r.append(d[cursor][0])
        cursor = d[cursor][direction]
    return r


def dump(d, start, direction=2):
    r = flatten_list(d, start, direction=direction)
    return ", ".join(f"{x}" for x in r)


def cmod(x, m):
    """
    Modulo, with C-like behavior.
    """
    return x - int(x / m) * m


def mix_round(d):
    z_index = np.argwhere(d[:, 0] == 0).flatten()[0]
    for offset in range(len(d)):
        x, p, n = d[offset]
        if x == 0:
            continue

        # Remove x
        d[p, 2] = n
        d[n, 1] = p

        x = cmod(x, len(d) - 1)
        # print("moving: ", x)
        direction = 2 if x > 0 else 1
        cursor = p if x > 0 else p
        # target = x if x > 0 else 1 - x
        for _ in range(abs(x)):
            cursor = d[cursor, direction]
        # print("   -", f"inserting after: {d[cursor, 0]} (before {d[d[cursor, 2], 0]})")

        tmp = d[cursor, 2]
        d[cursor, 2] = offset
        d[tmp, 1] = offset
        d[offset, 1] = cursor
        d[offset, 2] = tmp
        # print("   -", dump(d, z_index))
        # print("   -", dump(d, z_index, direction=1))


def part_1(seq):
    d = np.zeros((len(seq), 3), dtype=np.int32)
    for i, v in enumerate(seq):
        d[i] = [v, (i - 1) % len(seq), (i + 1) % len(seq)]
    zero_index = seq.index(0)
    mix_round(d)
    flat = flatten_list(d, zero_index)
    grooves_coordinates = [flat[d % len(seq)] for d in [1000, 2000, 3000]]
    return sum(grooves_coordinates)


def part_2(seq):
    d = np.zeros((len(seq), 3), dtype=np.int64)
    for i, v in enumerate(seq):
        d[i] = [811589153 * v, (i - 1) % len(seq), (i + 1) % len(seq)]
    for _ in trange(10):
        mix_round(d)
    flat = flatten_list(d, seq.index(0))
    grooves_coordinates = [flat[d % len(seq)] for d in [1000, 2000, 3000]]
    return sum(grooves_coordinates)


def aoc_inputs():
    return {
        "example": ("day20-input-ex", 3, 1623178306),
        "real": ("day20-input-1", 4151, 7848878698663)  # 988399382 too low, too high 8380469593878
    }
