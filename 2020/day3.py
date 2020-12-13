import numpy as np


def load_map(f):
    rows = []
    for line in f:
        rows.append(list(map(ord, line.strip())))
    return np.array(rows, dtype=np.uint8)


def vec2(x, y, dtype=np.int32):
    return np.array([x, y], dtype=dtype)


def count_trees(m, start, dir):
    p = start
    ym = m.shape[0]
    xm = m.shape[1]
    n_trees = 0
    while p[1] < ym:
        px, py = p
        if m[py, px] == ord('#'):
            n_trees += 1
        p += dir
        p[0] = p[0] % xm
    return n_trees


def aoc_run(filename='assets/day3-input'):
    m = load_map(open(filename))
    # print(m.shape, m)
    n_trees = count_trees(m, vec2(0, 0), vec2(3, 1))
    print("part 1:", n_trees)

    dirs = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    part_2 = 1
    for d in dirs:
        part_2 *= count_trees(m, vec2(0, 0), d)
    print("part 2:", part_2)


if __name__ == '__main__':
    aoc_run()
