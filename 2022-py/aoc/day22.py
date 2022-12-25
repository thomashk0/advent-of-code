# Skeleton for days
import re

import aoc

STEP_RE = re.compile(r"(\d+|[LR])")


def cvt(x):
    if x == "R" or x == "L":
        return x
    return int(x)


def rotate_l(p):
    return -p[1], p[0]


def rotate_r(p):
    return p[1], -p[0]


def adjacent(x, dirs):
    for dx, dy in dirs:
        yield x[0] + dx, x[1] + dy


def tuple_add(p, q):
    return tuple(x + y for x, y in zip(p, q))


def tuple_sub(p, q):
    return tuple(x - y for x, y in zip(p, q))


def parse_input(raw: str):
    m = {}
    lines = raw.splitlines()
    for i, line in enumerate(lines):
        if line == "":
            break
        for j, c in enumerate(line):
            if c != " ":
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


FACING_VALUE = {(0, 1): 0, (1, 0): 1, (0, -1): 2, (-1, 0): 3}


def get_password(cursor, direction):
    return 1000 * (1 + cursor[0]) + 4 * (1 + cursor[1]) + FACING_VALUE[direction]


def simulate(m, steps, cursor, apply_wrapping):
    direction = (0, 1)

    for p in steps:
        if p == "L":
            direction = rotate_l(direction)
        elif p == "R":
            direction = rotate_r(direction)
        else:
            for i in range(p):
                n_i, n_j = apply_wrapping(cursor, direction)
                if m[n_i, n_j] == "#":
                    break
                cursor = n_i, n_j
    return cursor, direction


def part_1(args):
    m, steps = args
    wi, wj = get_wraps(m)

    wraps = {}
    for j, (wmin, wmax) in enumerate(wi):
        wraps[wmax + 1, j, (1, 0)] = (wmin, j)
        wraps[wmin - 1, j, (-1, 0)] = (wmax, j)
    for i, (wmin, wmax) in enumerate(wj):
        wraps[i, wmax + 1, (0, 1)] = (i, wmin)
        wraps[i, wmin - 1, (0, -1)] = (i, wmax)

    cursor = (0, wj[0][0])

    def handle_wrap(src, dir):
        n_i = src[0] + dir[0]
        n_j = src[1] + dir[1]
        wrapped = wraps.get((n_i, n_j, dir))
        if wrapped is not None:
            return wrapped
        return n_i, n_j

    cursor, direction = simulate(m, steps, cursor, handle_wrap)
    return get_password(cursor, direction)


def scan_squares(m, start, width):
    cube_map = {start: "T"}
    dirs = [(-width, 0), (width, 0), (0, width), (0, -width)]
    to_explore = {start}
    explored = {}
    s_id = 1
    while len(to_explore) > 0:
        head = to_explore.pop()
        head_face = cube_map[head]
        explored[head] = s_id
        s_id += 1
        for d, (di, dj) in zip(adjacent(head, dirs), dirs):
            if d in explored:
                continue
            if d not in m:
                continue
            cube_map[d] = CUBE_MAP[head_face][di // width, dj // width]
            to_explore.add(d)
    return explored, cube_map


#  T
#  S
#  B
#  N
#  T
#  ENWSE
CUBE_MAP = {
    "T": {(-1, 0): "N", (1, 0): "S", (0, 1): "E", (0, -1): "W"},
    "N": {(-1, 0): "B", (1, 0): "T", (0, 1): "E", (0, -1): "W"},
    "S": {(-1, 0): "T", (1, 0): "B", (0, 1): "E", (0, -1): "W"},
    "B": {(-1, 0): "S", (1, 0): "N", (0, 1): "E", (0, -1): "W"},
    "E": {(-1, 0): "T", (1, 0): "B", (0, 1): "N", (0, -1): "S"},
    "W": {(-1, 0): "T", (1, 0): "B", (0, 1): "S", (0, -1): "N"}
}


def cube_wrap(cube_origins, cube_ids, src, d, square_width):
    q = tuple_add(src, d)
    if q in cube_ids:
        return q
    # PHASE0: wrap inside the cube, then translate.
    cube_offset = tuple_sub(q, cube_origins[cube_ids[src]])
    wrapped = cube_offset[0] % square_width, cube_offset[1] % square_width
    new_cube = CUBE_MAP[cube_ids[src]][d]
    new_loc = tuple_add(cube_origins[new_cube], wrapped)
    return new_loc


def part_2(args):
    m, steps = args
    wi, wj = get_wraps(m)

    square_width = 4
    cursor = (0, wj[0][0])
    squares, cube_map = scan_squares(m, cursor, square_width)
    print("cube_map:", cube_map)
    debug = {}
    for loc, s_id in squares.items():
        ch = cube_map[loc]
        for i in range(square_width):
            for j in range(square_width):
                debug[loc[0] + i, loc[1] + j] = ch

    print("squares:", squares)
    cube_origins = {v: k for k, v in cube_map.items()}
    print("origins:", cube_origins)
    d = aoc.SparseMap({(j, i): v for (i, j), v in debug.items()}, default=" ")
    print(d.draw())

    def handle_wrap(src, dir):
        return cube_wrap(cube_origins, debug, src, dir, square_width)

    cursor = (0, wj[0][0])
    cursor, direction = simulate(m, steps, cursor, handle_wrap)
    return get_password(cursor, direction)

    return 2 * len(args)


def aoc_inputs():
    return {
        "example": ("day22-input-ex", 6032, 8),
        # "real": ("day22-input-1", 164014, None),
    }
