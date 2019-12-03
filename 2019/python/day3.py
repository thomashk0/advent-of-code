M = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}


def get_coverage(path):
    points = set()
    dist = {}
    step = 0
    lx, ly = 0, 0
    for d in path:
        xm, ym = M[d[0]]
        lx, ly
        for i in range(int(d[1:])):
            lx += xm
            ly += ym
            step += 1
            dist[(lx, ly)] = step
            points.add((lx, ly))
    return points, dist


def l1_dist(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def solve(w1, w2):
    i = get_coverage(w1)[0] & get_coverage(w2)[0]
    return min(l1_dist((0, 0), p) for p in i)


def test(w1, w2, expected):
    assert solve(w1.split(','), w2.split(',')) == expected


def main():
    test("R8,U5,L5,D3", "U7,R6,D4,L4", 6)
    test("R75,D30,R83,U83,L12,D49,R71,U7,L72",
         "U62,R66,U55,R34,D71,R55,D58,R83", 159)
    test("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
         "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 135)

    with open('assets/day3-input') as f:
        w1 = f.readline().split(',')
        w2 = f.readline().split(',')

    print("part 1:", solve(w1, w2))
    s1, d1 = get_coverage(w1)
    s2, d2 = get_coverage(w2)
    print("part 2:", min(d1[p] + d2[p] for p in s1 & s2))


if __name__ == '__main__':
    main()
