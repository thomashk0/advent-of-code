# Skeleton for days
import re

STEP_RE = re.compile(r"(\d+|[LR])")


def cvt(x):
    if x == 'R' or x == 'L':
        return x
    return int(x)


def rotate_l(p):
    return -p[1], p[0]


def rotate_r(p):
    return p[1], -p[0]


def parse_input(raw: str):
    m = {}
    lines = raw.splitlines()
    for i, line in enumerate(lines):
        if line == "":
            break
        for j, c in enumerate(line):
            if c != ' ':
                m[i, j] = c
    print(lines[-1])
    steps = list(map(cvt, STEP_RE.findall(lines[-1])))
    return m, steps


def get_wraps(m):
    x_max = max(x[1] for x in m.keys())
    y_max = max(x[0] for x in m.keys())
    wraps_y = [[y_max, 0] for _ in range(x_max + 1)]
    wraps_x = [[x_max, 0] for _ in range(y_max + 1)]
    for y, x in m.keys():
        wy = wraps_y[x]
        if y < wy[0]:
            wraps_y[x][0] = y
        elif y > wy[1]:
            wraps_y[x][1] = y

        wx = wraps_x[y]
        if x < wx[0]:
            wraps_x[y][0] = x
        elif x > wx[1]:
            wraps_x[y][1] = x
    return wraps_y, wraps_x


FACING_VALUE = {
    (0, 1): 0,
    (1, 0): 1,
    (0, -1): 2,
    (-1, 0): 3
}


def part_1(args):
    m, steps = args
    wi, wj = get_wraps(m)

    cursor = (0, wj[0][0])
    direction = (0, 1)
    print(rotate_l(direction))
    print(rotate_r(direction))

    for p in steps:
        if p == 'L':
            direction = rotate_l(direction)
        elif p == 'R':
            direction = rotate_r(direction)
        else:
            for i in range(p):
                c_i, c_j = cursor
                n_i = cursor[0] + direction[0]
                n_j = cursor[1] + direction[1]

                # if 0 <= n_j <= len(wi):
                if n_i < wi[c_j][0]:
                    n_i = wi[c_j][1]
                if n_i > wi[c_j][1]:
                    n_i = wi[c_j][0]
                # if 0 <= n_i <= len(wj):
                if n_j < wj[c_i][0]:
                    n_j = wj[c_i][1]
                if n_j > wj[c_i][1]:
                    n_j = wj[c_i][0]

                if m[n_i, n_j] == "#":
                    break
                cursor = n_i, n_j
    print(f"final state: cursor={cursor}, facing={direction}")

    return 1000 * (1 + cursor[0]) + 4 * (1 + cursor[1]) + FACING_VALUE[direction]


def part_2(input):
    return 2 * len(input)


def aoc_inputs():
    return {
        "example": ("day22-input-ex", 6032, 8),
        "real": ("day22-input-1", None, None)
    }
