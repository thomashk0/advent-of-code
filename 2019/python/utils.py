import copy

import networkx as nx

DIRS_2D = {'L': (-1, 0), 'R': (1, 0), 'N': (0, -1), 'S': (0, 1)}


def neighbours(p):
    x, y = p
    return ((i, (x + dx, y + dy)) for i, (dx, dy) in DIRS_2D.items())


def d1(p, q):
    """Manhattan distance (L1)"""
    return sum(abs(x - y) for x, y in zip(p, q))


def d2(p, q):
    """Squared Euclidian distance (L2)"""
    return sum(abs(x - y) for x, y in zip(p, q))


def limits(m, dims=2):
    def f():
        for i in range(dims):
            imin = min(x[i] for x in m)
            imax = max(x[i] for x in m)
            yield imin, imax

    return tuple(f())


# class SparseMapView:
#     def __init__(self, other, xmin=None, xmax=None, ymin=None, ymax=None):
#         self.xmin = xmin
#         self.xmax = xmax
#         self.ymin = ymin
#         self.ymax = ymax
#         self._map = other
#
#     def __delitem__(self, key):
#         del self._map[key]
#
#     def __setitem__(self, key, value):
#         self._map[key] = value
#
#     def __getitem__(self, item):
#         xs, ys = item
#         if isinstance(xs, int) and isinstance(ys, int):
#             return self._map[item]
#
#     def get(self, default=None):
#         self._map.get(default)
#
#     def draw(self, fill_char=' '):
#         self._map.draw()
#
#     def limits(self):
#         return limits(self._map.keys())


class SparseMap:
    def __init__(self, data=None, ignored=None, floor_tiles=None):
        self.data = data or dict()
        self.ignored = ignored or set()
        self.floor_tile = floor_tiles or {'.'}

    def __copy__(self):
        other = SparseMap(ignored=copy.copy(self.ignored),
                          floor_tiles=copy.copy(self.floor_tile))
        other.data = self.data.copy()
        return other

    def copy(self):
        return copy.copy(self)

    def limits(self):
        if len(self.data) == 0:
            return (0, 0), (0, 0)
        return limits(self.data.keys())

    def items(self):
        return self.data.items()

    def __delitem__(self, key):
        del self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, item):
        return self.data[item]

    def get(self, key, default=None):
        return self.data.get(key, default)

    def show(self, fill_char=' '):
        (xmin, xmax), (ymin, ymax) = self.limits()
        return "\n".join("".join(
            self.data.get((x, y), fill_char) for x in range(xmin, xmax + 1)) for
                         y in range(ymin, ymax + 1))

    def draw(self, fill_char=' '):
        (xmin, xmax), (ymin, ymax) = limits(self.data.keys())
        for y in range(ymin, ymax + 1):
            print(
                "".join(self.data.get((x, y), fill_char) for x in
                        range(xmin, xmax + 1)))

    @classmethod
    def from_list(cls, data, ignored=None):
        d = {}
        for i, row in enumerate(data):
            for j, c in enumerate(row):
                if c in ignored:
                    continue
                d[(j, i)] = c
        return cls(d, ignored)

    @classmethod
    def from_file(cls, f_name, ignored=None):
        ignored = ignored or {' ', '\n', '\t'}
        with open(f_name) as f:
            return cls.from_list([list(l.rstrip()) for l in f], ignored)


if __name__ == '__main__':
    m = SparseMap.from_file("assets/day20-example-0")
    m.draw()
    print(m[5, 5])
    # print(m[5:, 3:])
