import itertools
import math


def l2_norm(p):
    return math.sqrt(p[0] ** 2 + p[1] ** 2)


def angle(p):
    """
    >>> angle((0, -1)) == 0
    True
    >>> angle((1, 0)) == math.pi / 2
    True
    >>> angle((0, 1)) == math.pi
    True
    >>> angle((-1, 0)) == 3*math.pi / 2
    True
    """
    x = math.acos(-p[1] / l2_norm(p))
    return x if p[0] >= 0 else 2 * math.pi - x


def read_map(f):
    for i, l in enumerate(f):
        for j, c in enumerate(l.strip()):
            if c == '#':
                yield j, i


def detectable_dirs(m, p):
    view_dirs = set()
    for q in m:
        if q == p:
            continue
        d0, d1 = q[0] - p[0], q[1] - p[1]
        gcd = math.gcd(d0, d1)
        view_dirs.add((d0 // gcd, d1 // gcd))
    return view_dirs


def num_detectable(m, p):
    return len(detectable_dirs(m, p))


def part_1(f_name):
    with open(f_name) as f:
        coords = list(read_map(f))
        return max(((num_detectable(coords, p), p) for p in coords),
                   key=lambda x: x[0])


def next_hit(coords, origin, v, n=100):
    ox, oy = origin
    vx, vy = v
    for i in range(1, n):
        dst = (ox + i * vx, oy + i * vy)
        # print(dst)
        if dst in coords:
            return dst
    return None


def part_2(f_name, debug=False):
    _, best = part_1(f_name)
    with open(f_name) as f:
        coords = set(read_map(f))
        ds = list(detectable_dirs(coords, best))
        ds.sort(key=lambda p: angle(p))
        # for p in ds:
        #     print(p, angle(p))
        for i, d in zip(range(200), itertools.cycle(ds)):
            tgt = next_hit(coords, best, d)
            if debug:
                print(f"{i + 1:2d}: {tgt} (angle={d})")
            coords.remove(tgt)
        return tgt


def main():
    with open('assets/day10-example-4') as f:
        coords = list(read_map(f))
        assert num_detectable(coords, (3, 4)) == 8
        assert num_detectable(coords, (4, 2)) == 5
        assert num_detectable(coords, (3, 2)) == 7
        assert num_detectable(coords, (3, 2)) == 7
    assert part_1('assets/day10-example-0')[0] == 33
    assert part_1('assets/day10-example-1')[0] == 35
    assert part_1('assets/day10-example-2')[0] == 41
    assert part_1('assets/day10-example-3')[0] == 210
    print("part 1:", part_1('assets/day10-input'))

    assert part_2('assets/day10-example-3') == (8, 2)
    hi, lo = part_2('assets/day10-input')
    print("part 2:", hi * 100 + lo)


if __name__ == '__main__':
    main()
