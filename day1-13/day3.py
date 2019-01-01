import re
import sys
import itertools
import collections


def rectangle(r):
    return itertools.product(range(r.x, r.x + r.w), range(r.y, r.y + r.h))


def main():
    regex = re.compile("#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
    Request = collections.namedtuple('Request', ['req_id', 'x', 'y', 'w', 'h'])
    requests = []
    carto = collections.Counter()
    for l in sys.stdin:
        r = Request(*map(int, regex.match(l.strip()).groups()))
        requests.append(r)
        carto.update((x, y) for x, y in rectangle(r))

    print("Part 1:", len([p for p, cnt in carto.items() if cnt > 1]))
    for r in requests:
        if all(carto[(x, y)] == 1 for x, y in rectangle(r)):
            print("Part 2:", r.req_id)


if __name__ == '__main__':
    main()
