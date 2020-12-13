def parse_ids(line):
    return [None if x == 'x' else int(x) for x in line.split(",")]


def run_part_2(line):
    ids = [(i, x) for i, x in enumerate(parse_ids(line)) if x is not None]
    return part_2(ids)


def parse_input(lines):
    target = int(next(lines))
    return target, parse_ids(next(lines))


def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def pmod(x, d):
    r = x % d
    if r < 0:
        r += d
    return r


def mod_inv(x, d):
    g, u, _ = xgcd(x, d)
    assert g == 1, "not invertible"
    assert (u * x) % d == 1, "inversion failed"
    if u < 0:
        u += d
    return u


def update(p, q):
    px, py = p
    qx, qy = q
    r = pmod(mod_inv(px, qx) * (qy - py), qx)
    return (px * qx, px * r + py)


def part_2(ids):
    coeffs = [(n, pmod(-i, n)) for i, n in ids]
    acc = coeffs[0]
    for p in coeffs[1:]:
        acc = update(acc, p)
        # print(acc)
    return acc[1]


def test_part2():
    assert run_part_2("17,x,13,19") == 3417
    assert run_part_2("67,7,59,61") == 754018
    assert run_part_2("1789,37,47,1889") == 1202161486


def aoc_run(input_path):
    target, ids = parse_input(open(input_path))
    ids_2 = [(i, x) for i, x in enumerate(ids) if x is not None]
    ids = [x for x in ids if x is not None]
    # print(target, ids)
    r = [(x, x - (target % x)) for x in ids]
    x, xm = min(r, key=lambda v: v[1])
    print("part 1:", xm * x)
    print("part 2:", part_2(ids_2))


if __name__ == '__main__':
    aoc_run('assets/day13-input')
