import intcpu

import networkx as nx

DIR_MAP = {1: (0, 1), 2: (0, -1), 3: (-1, 0), 4: (1, 0)}


def neightbours(p):
    x, y = p
    return ((i, (x + dx, y + dy)) for i, (dx, dy) in DIR_MAP.items())


class CpuHalted(Exception):
    pass


def limits(m):
    def f():
        for i in range(2):
            imin = min(x[i] for x in m)
            imax = max(x[i] for x in m)
            yield imin, imax

    return tuple(f())


def draw(m):
    (xmin, xmax), (ymin, ymax) = limits(list(m))
    for y in reversed(range(ymin, ymax + 1)):
        print("".join(m.get((x, y), ' ') for x in range(xmin, xmax + 1)))


class Droid:
    def __init__(self, src=None, cpu=None):
        self.cpu = cpu or intcpu.IntCpu()
        if src:
            self.cpu.load_file(src)
        self.loc = (0, 0)

    def clone(self):
        d = Droid(cpu=self.cpu.clone())
        d.loc = self.loc
        return d

    def _step(self, d):
        self.cpu.add_input(d)
        while True:
            ret = self.cpu.step()
            if ret == 1:
                raise CpuHalted()
            if ret == 2:
                raise Exception("No input to be provided")
            o = self.cpu.pop_output()
            if o is not None:
                return o

    def step(self, d):
        o = self._step(d)
        x, y = self.loc
        dx, dy = DIR_MAP[d]
        if o == 1 or o == 2:
            self.loc = (x + dx, y + dy)
        return o


def spread(start_droid, start_tile=' '):
    world = {start_droid.loc: start_tile}
    droids = [start_droid.clone()]
    g = nx.Graph()
    while len(droids) > 0:
        next_generation = []
        for droid in droids:
            for d, n in neightbours(droid.loc):
                if n in world:
                    continue
                r = droid.clone()
                o = r.step(d)
                if o == 0:
                    world[n] = '#'
                else:
                    world[n] = 'O' if o == 2 else ' '
                    g.add_edge(droid.loc, n)
                    next_generation.append(r)
        droids = next_generation
    return g, world


def tree_height(t, n):
    succ = list(t.successors(n))
    if len(succ) == 0:
        return 1
    return 1 + max([tree_height(t, s) for s in succ])


def main():
    import pprint
    droid = Droid("../assets/day15-input")
    g, m = spread(droid, ' ')

    oxygen_location = next(coords for coords, t in m.items() if t == 'O')
    path = nx.shortest_path(g, source=(0, 0), target=oxygen_location)
    print("part 1:", len(path) - 1)
    t = nx.bfs_tree(g, source=oxygen_location)
    assert nx.is_tree(t)
    print("part 2:", tree_height(t, oxygen_location) - 1)


if __name__ == "__main__":
    main()
