import sys
import itertools
import collections


def manhattan_distance(p, q):
    return sum([abs(pc - qc) for pc, qc in zip(p, q)])


SHIFTS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def neighbourgs(p):
    x, y = p
    for dx, dy in SHIFTS:
        yield x + dx, y + dy


def expand(state, limits, is_infinite, update):
    update_next = set()
    xmin, xmax, ymin, ymax = limits
    for p in update:
        px, py = p
        distance, owner = state[p]
        if px < xmin or px > xmax or py < ymin or py > ymax:
            is_infinite.add(owner)
            continue
        for v in neighbourgs(p):
            if v in state:
                d, other = state[v]
                if distance + 1 == d and other != owner:
                    state[v] = (d, '.')
                elif d < distance + 1:
                    pass
                else:
                    state[v] = (distance + 1, owner)
                    update_next.add(v)
            else:
                state[v] = (distance + 1, owner)
                update_next.add(v)
    return update_next


def main():
    coords = [tuple(map(int, l.split(','))) for l in sys.stdin]
    xmin, xmax = min(coords, key=lambda x: x[0])[0], \
                 max(coords, key=lambda x: x[0])[0]
    ymin, ymax = min(coords, key=lambda x: x[1])[1], \
                 max(coords, key=lambda x: x[1])[1]
    state = {c: (0, i) for i, c in enumerate(coords)}
    to_update = set(state.keys())
    is_infinite = set()

    for i in range(10000):
        to_update = expand(state, (xmin, xmax, ymin, ymax), is_infinite,
                           to_update)
        if len(to_update) == 0:
            print("End of simulation")
            break
    cnt = collections.Counter(
        i for _, i in state.values() if i not in is_infinite)
    print("Part 1:", cnt.most_common(1)[0][1])

    total = sum(
        sum(manhattan_distance((x, y), p) for p in coords) < 10000
        for x, y in itertools.product(range(xmin, xmax + 1),
                                      range(ymin, ymax + 1)))
    print("Part 2:", total)


if __name__ == '__main__':
    main()
