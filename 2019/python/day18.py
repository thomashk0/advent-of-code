import heapq
import itertools
import pprint
import networkx as nx

DIR_MAP = {'L': (0, -1), 'R': (0, 1), 'U': (-1, 0), 'D': (1, 0)}


def parse(f_name):
    with open(f_name) as f:
        return [list(l.strip()) for l in f]


def neightbours(p):
    x, y = p
    return ((i, (x + dx, y + dy)) for i, (dx, dy) in DIR_MAP.items())


def search(m, target):
    l = [(i, j) for i, row in enumerate(m) for j, c in enumerate(row) if
         c == target]
    if len(l) > 0:
        return l
    return []


def replace(m, c, c_next):
    loc = search(m, c)
    if loc:
        m[loc[0]][loc[1]] = c_next


def draw(m):
    print("\n".join("".join(l) for l in m))


def build_graph(m, entry):
    def is_reachable(p):
        px, py = p
        c = m[px][py]
        if c == '#':
            return False
        return True

    to_explore = {entry}
    explored = set()
    g = nx.Graph()
    while len(to_explore) > 0:
        p = to_explore.pop()
        c = m[p[0]][p[1]]
        if p in explored:
            continue
        if c.isupper():
            g.add_node(p, door=c)
        if c.islower():
            g.add_node(p, key=c)
        explored.add(p)
        for d, n in neightbours(p):
            if is_reachable(n):
                g.add_edge(p, n, dir=d)
                to_explore.add(n)
    return g


def graph_data(g, label):
    return ((c, k) for c, k in g.nodes.data(label) if k)


def build_deps(g, start):
    deps = {k: set() for _, k in graph_data(g, 'key')}
    for (n, door) in graph_data(g, 'door'):
        g_mod = g.copy(as_view=False)
        g_mod.remove_node(n)
        for (s, k) in graph_data(g, 'key'):
            if not nx.has_path(g_mod, start, s):
                deps[k].add(door.lower())
    return deps


def min_path(g, start):
    key_dep = build_deps(g, start)
    key_loc = {k: c for c, k in graph_data(g, 'key')}
    paths = {}

    def get_path(s, d):
        if (s, d) not in paths:
            paths[(s, d)] = nx.shortest_path(g, s, d)
        return len(paths[(s, d)]) - 1

    cache = {}

    def solve(p, keys):
        e = p, "".join(sorted(keys))
        if e not in cache:
            cache[e] = solve_(p, keys)
        return cache[e]

    def solve_(p, keys):
        ks = [k for k, deps in key_dep.items() if
              (k not in keys) and (len(deps - keys) == 0)]
        if len(ks) == 0:
            return 0
        scores = []
        for k in ks:
            n = get_path(p, key_loc[k])
            r = solve(key_loc[k], keys | {k})
            scores.append((k, n + r))
        best = min(scores, key=lambda x: x[1])
        return best[1]

    return solve(start, set())


def min_path_2(g, robots, key_dep, reachable):
    key_loc = {k: c for c, k in graph_data(g, 'key')}
    paths = {}

    def get_path(s, d):
        if (s, d) not in paths:
            paths[(s, d)] = nx.shortest_path(g, s, d)
        return len(paths[(s, d)]) - 1

    cache = {}

    def solve(p, keys):
        e = p, "".join(sorted(keys))
        if e not in cache:
            cache[e] = solve_(p, keys)
        return cache[e]

    def solve_(p, keys):
        ks = [k for k, deps in key_dep.items() if
              (k not in keys) and (len(deps - keys) == 0)]
        if len(ks) == 0:
            return 0
        scores = []
        for k in ks:
            r_id = reachable[k]
            robot = p[r_id]
            r2 = list(p)
            r2[r_id] = key_loc[k]
            n = get_path(robot, key_loc[k])
            r = solve(tuple(r2), keys | {k})
            scores.append((k, n + r))

        best = min(scores, key=lambda x: x[1])
        return best[1]

    return solve(robots, set())


def part_1(f_name, **kwargs):
    m = parse(f_name)
    start = search(m, '@')[0]
    m[start[0]][start[1]] = '.'
    # draw(m)
    g = build_graph(m, start)
    return min_path(g, start, **kwargs)


def part_2(f_name, **kwargs):
    m = parse(f_name)
    sy, sx = search(m, '@')[0]
    m[sy][sx] = '.'
    g = build_graph(m, (sy, sx))
    deps = build_deps(g, (sy, sx))
    for y in range(-1, 2):
        for x in range(-1, 2):
            m[sy + y][sx + x] = '#'
    for y, x in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        m[sy + y][sx + x] = '.'
    robots = [(y + sy, x + sy) for x, y in [(-1, -1), (-1, 1), (1, -1), (1, 1)]]

    gs = [build_graph(m, r) for r in robots]
    reachable = {}
    for i, g in enumerate(gs):
        for _, k in graph_data(g, 'key'):
            reachable[k] = i
    g = nx.Graph()
    for g_n in gs:
        g = nx.union(g, g_n)
    # draw(m)
    return min_path_2(g, tuple(robots), deps, reachable)


def main():
    assert part_1("assets/day18-example-4") == 86
    assert part_1("assets/day18-example-0") == 132
    assert part_1("assets/day18-example-2") == 81
    assert part_1("assets/day18-example-1") == 136
    print("part 1:", part_1("assets/day18-input"))
    print("part 2:", part_2("assets/day18-input"))
    return


if __name__ == '__main__':
    main()
