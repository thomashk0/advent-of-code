import itertools
import networkx as nx

DIR_MAP = {'L': (-1, 0), 'R': (1, 0), 'U': (0, -1), 'D': (0, 1)}


def neightbours(p):
    x, y = p
    return ((i, (x + dx, y + dy)) for i, (dx, dy) in DIR_MAP.items())


def d1(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def draw(m):
    (xmin, xmax), (ymin, ymax) = limits(list(m))
    for y in range(ymin, ymax + 1):
        print("".join(m.get((x, y), ' ') for x in range(xmin, xmax + 1)))


def load(lines):
    m = {}
    for i, row in enumerate(lines):
        for j, c in enumerate(row):
            if c == ' ':
                continue
            m[(j, i)] = c
    return m


def limits(m):
    def f():
        for i in range(2):
            imin = min(x[i] for x in m)
            imax = max(x[i] for x in m)
            yield imin, imax

    return tuple(f())


def parse(f_name):
    with open(f_name) as f:
        return load([list(l.rstrip()) for l in f])


def scan_portals(m):
    (xmin, xmax), (ymin, ymax) = limits(m)
    portals = []
    # Horizontal scan
    for y in range(ymin, ymax + 1):
        current_patt = []
        for x in range(xmin, xmax + 2):
            c = m.get((x, y), ' ')
            if c.isalpha():
                current_patt.append((c, (x, y)))
            else:
                if len(current_patt) > 1:
                    portals.append(current_patt)
                current_patt = []
    # Vertical scan
    for x in range(xmin, xmax + 1):
        current_patt = []
        for y in range(ymin, ymax + 2):
            c = m.get((x, y), ' ')
            if c.isalpha():
                current_patt.append((c, (x, y)))
            else:
                if len(current_patt) > 1:
                    portals.append(current_patt)
                current_patt = []

    portal_map = {}
    for p in portals:
        label = "".join(c for c, _ in p)
        for i in [0, -1]:
            for _, n in neightbours(p[i][1]):
                if m.get(n, ' ') == '.':
                    if label not in portal_map:
                        portal_map[label] = [n]
                    else:
                        portal_map[label].append(n)
    return portal_map


def build_graph(m, portals, with_shortcuts=True):
    shortcuts = {}
    for p in portals.values():
        if len(p) != 2:
            continue
        src, dst = tuple(p)
        assert src not in shortcuts
        other = shortcuts.get(dst)
        assert other is None
        shortcuts[src] = dst
        shortcuts[dst] = src

    to_explore = {portals['AA'][0]}
    explored = set()
    g = nx.DiGraph()
    while to_explore:
        n = to_explore.pop()
        if n in explored:
            continue
        explored.add(n)
        for direction, s in neightbours(n):
            if m.get(s) == '.':
                g.add_edge(n, s, direction=direction)
                to_explore.add(s)
        d = shortcuts.get(n)
        if d:
            if with_shortcuts:
                g.add_edge(n, d, is_shortcut=True)
            to_explore.add(d)

    return g


def part_1(f_name):
    m = parse(f_name)
    portals = scan_portals(m)
    # print(portals)

    g = build_graph(m, portals)
    p = nx.shortest_path(g, portals['AA'][0], portals['ZZ'][0])
    for coords in p:
        m[coords] = '*'
    # draw(m)
    return len(p) - 1


def main():
    assert part_1("assets/day20-example-0") == 23
    assert part_1("assets/day20-example-1") == 58
    print("part 1:", part_1("assets/day20-input"))


if __name__ == '__main__':
    main()
