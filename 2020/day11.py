import itertools


class SparseMap:
    def __init__(self, data, default):
        self.default = default
        self.data = data
        self._limits = self.limits()

    def limits(self):
        xs = [x for x, _ in self.data.keys()]
        ys = [y for _, y in self.data.keys()]
        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)
        return (xmin, xmax), (ymin, ymax)

    @classmethod
    def from_lines(cls, lines, default=' '):
        data = {}
        for line_num, line in enumerate(lines):
            for col_num, char in enumerate(line.strip()):
                data[(line_num, col_num)] = char
        return cls(data, default)

    def __getitem__(self, item):
        return self.data.get(item, self.default)

    def __setitem__(self, key, value):
        self.data[key] = value


ADJACENT = [(xd, yd) for xd, yd in itertools.product([-1, 0, 1], [-1, 0, 1])
            if xd != 0 or yd != 0]


def step(state, is_occupied, empty_threshold):
    new_state = {}
    for (x, y), c in state.data.items():
        n_occupied = sum(is_occupied(state, (x, y), dir) for dir in ADJACENT)
        if c == 'L' and n_occupied == 0:
            new_state[(x, y)] = '#'
        elif c == '#' and n_occupied >= empty_threshold:
            new_state[(x, y)] = 'L'
        else:
            new_state[(x, y)] = c
    changed = new_state != state.data
    state.data = new_state
    return changed


def solve(input_path, is_occupied, empty_threshold):
    m = SparseMap.from_lines(open(input_path))
    n_iteration = 0
    while step(m, is_occupied, empty_threshold):
        n_iteration += 1
    return sum(x == '#' for x in m.data.values())


def is_occupied(state, p, dir):
    px, py = p
    dx, dy = dir
    return state[(px + dx, py + dy)] == '#'


def occupied_along(state, start, dir):
    px, py = start
    dx, dy = dir
    while True:
        px += dx
        py += dy
        c = state[(px, py)]
        if c == '#':
            return True
        elif c == 'L':
            return False
        elif c != '.':
            return False


def aoc_run(filename='assets/day11-input'):
    print("part 1:", solve(filename, is_occupied, 4))
    print("part 2:", solve(filename, occupied_along, 5))
    return


if __name__ == '__main__':
    aoc_run()
