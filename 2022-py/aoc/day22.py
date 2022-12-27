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
                (n_i, n_j), new_dir = apply_wrapping(cursor, direction)
                if m[n_i, n_j] == "#":
                    break
                if new_dir is not None:
                    direction = new_dir
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
            return wrapped, None
        return (n_i, n_j), None

    cursor, direction = simulate(m, steps, cursor, handle_wrap)
    return get_password(cursor, direction)


def scan_squares(m, start, width):
    dirs = [(-width, 0), (width, 0), (0, width), (0, -width)]
    to_explore = {start}
    explored = {}
    s_id = 1
    while len(to_explore) > 0:
        head = to_explore.pop()
        explored[head] = s_id
        s_id += 1
        for d in adjacent(head, dirs):
            if d in explored:
                continue
            if d not in m:
                continue
            to_explore.add(d)
    return explored


def part_2(args):
    m, steps = args
    wi, wj = get_wraps(m)

    square_width = 50
    cursor = (0, wj[0][0])
    squares = scan_squares(m, cursor, square_width)
    # print("cube_map:", cube_map)
    debug = {}
    for loc, s_id in squares.items():
        # ch = cube_map[loc]
        for i in range(square_width):
            for j in range(square_width):
                debug[loc[0] + i, loc[1] + j] = s_id
    print("squares:", squares)
    squares_origins = {v: k for k, v in squares.items()}
    print("square origins:", squares_origins)

    # cube_origins = {v: k for k, v in cube_map.items()}
    # print("origins:", cube_origins)
    # d = aoc.SparseMap({(j, i): str(v) for (i, j), v in debug.items()}, default=" ")
    # print(d.draw())

    def handle_wrap(src, dir):
        p = tuple_add(src, dir)
        if p in debug:
            return p, None
        delta = tuple_sub(src, squares_origins[debug[src]])
        if debug[src] == 1 and dir == (-1, 0):
            cube = squares_origins[6]
            return (cube[0] + delta[1], cube[1]), (0, 1)
        if debug[src] == 1 and dir == (0, -1):
            cube = squares_origins[5]
            return (cube[0] + square_width - 1 - delta[0], cube[1]), (0, 1)
        if debug[src] == 6 and dir == (0, -1):
            cube = squares_origins[1]
            return (cube[0], cube[1] + delta[0]), (1, 0)
        if debug[src] == 5 and dir == (0, -1):
            cube = squares_origins[1]
            return (cube[0] + square_width - 1 - delta[0], cube[1]), (0, 1)
        if debug[src] == 5 and dir == (-1, 0):
            cube = squares_origins[2]
            return (cube[0] + delta[1], cube[1]), (0, 1)
        if debug[src] == 2 and dir == (0, -1):
            cube = squares_origins[5]
            return (cube[0], cube[1] + delta[0]), (1, 0)
        if debug[src] == 2 and dir == (0, 1):
            cube = squares_origins[4]
            return (cube[0] + square_width - 1, cube[1] + delta[0]), (-1, 0)
        if debug[src] == 4 and dir == (0, 1):
            cube = squares_origins[3]
            return (
                cube[0] + square_width - 1 - delta[0],
                cube[1] + square_width - 1,
            ), (0, -1)
        if debug[src] == 6 and dir == (1, 0):
            cube = squares_origins[4]
            return (cube[0], cube[1] + delta[1]), (1, 0)
        if debug[src] == 6 and dir == (0, 1):
            cube = squares_origins[3]
            return (cube[0] + square_width - 1, cube[1] + delta[0]), (-1, 0)
        if debug[src] == 4 and dir == (1, 0):
            cube = squares_origins[2]
            return (cube[0] + delta[1], cube[1] + square_width - 1), (0, -1)
        if debug[src] == 3 and dir == (1, 0):
            cube = squares_origins[6]
            return (cube[0] + delta[1], cube[1] + square_width - 1), (0, -1)
        if debug[src] == 3 and dir == (0, 1):
            cube = squares_origins[4]
            return (
                cube[0] + square_width - 1 - delta[0],
                cube[1] + square_width - 1,
            ), (0, -1)
        if debug[src] == 4 and dir == (-1, 0):
            cube = squares_origins[6]
            return (cube[0] + square_width - 1, cube[1] + delta[1]), (-1, 0)
        raise NotImplemented()

    cursor = (0, wj[0][0])
    cursor, direction = simulate(m, steps, cursor, handle_wrap)
    return get_password(cursor, direction)


def aoc_inputs():
    return {
        "real": ("day22-input-1", 164014, 47525),
    }
