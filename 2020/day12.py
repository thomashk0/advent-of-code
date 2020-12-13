def mdist(p, q):
    px, py = p
    qx, qy = q
    return abs(px - qx) + abs(py - qy)


def parse_input(lines):
    for l in lines:
        dir = l[0]
        cnt = int(l[1:])
        yield dir, cnt


def rotate_l(d, degrees):
    dx, dy = d
    while degrees > 0:
        dx, dy = dy, -dx
        degrees -= 90
    return dx, dy


def rotate_r(d, degrees):
    dx, dy = d
    while degrees > 0:
        dx, dy = -dy, dx
        degrees -= 90
    return dx, dy


def move_part_1(lines):
    px, py = 0, 0
    dx, dy = 1, 0
    for d, cnt in lines:
        if d in "EWNSF":
            if d == 'E':
                ndx, ndy = 1, 0
            elif d == 'W':
                ndx, ndy = -1, 0
            elif d == 'N':
                ndx, ndy = 0, -1
            elif d == 'S':
                ndx, ndy = 0, 1
            elif d == 'F':
                ndx, ndy = dx, dy
            else:
                raise ValueError()
            px += cnt * ndx
            py += cnt * ndy
        elif d == 'L':
            dx, dy = rotate_l((dx, dy), cnt)
        elif d == 'R':
            dx, dy = rotate_r((dx, dy), cnt)
        else:
            raise ValueError()
        # print(f"(px={px:3}, py={py:3}), ({dx:3}, {dy:3})")
    return px, py


def move_part_2(lines, wp):
    px, py = 0, 0
    wpx, wpy = wp
    dx, dy = 1, 0
    for d, cnt in lines:
        if d in "EWNS":
            if d == 'E':
                ndx, ndy = 1, 0
            elif d == 'W':
                ndx, ndy = -1, 0
            elif d == 'N':
                ndx, ndy = 0, -1
            elif d == 'S':
                ndx, ndy = 0, 1
            else:
                raise ValueError()
            wpx += cnt * ndx
            wpy += cnt * ndy
        elif d == 'F':
            ndx, ndy = wpx - px, wpy - py
            px += cnt * ndx
            py += cnt * ndy
            wpx += cnt * ndx
            wpy += cnt * ndy
        else:
            ndx, ndy = wpx - px, wpy - py
            if d == 'L':
                ndx, ndy = rotate_l((ndx, ndy), cnt)
            elif d == 'R':
                ndx, ndy = rotate_r((ndx, ndy), cnt)
            else:
                raise ValueError()
            wpx = px + ndx
            wpy = py + ndy
    return px, py


def aoc_run(filename='assets/day12-input'):
    steps = list(parse_input(open(filename)))
    print("part 1:", mdist((0, 0), move_part_1(steps)))
    print("part 2:", mdist((0, 0), move_part_2(steps, (10, -1))))


if __name__ == '__main__':
    aoc_run()
