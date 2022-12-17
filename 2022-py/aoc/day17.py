from aoc import SparseMap

ROCK_PATTERNS = [
    [[1, 1, 1, 1]],
    [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
    [[0, 0, 1], [0, 0, 1], [1, 1, 1]],
    [[1], [1], [1], [1]],
    [[1, 1], [1, 1]],
]


def parse_input(raw: str):
    return list(raw.strip())


def collides(m, pattern, pattern_offset):
    px, py = pattern_offset
    if py <= 0:
        return True
    if px < 0 or px + len(pattern[0]) > 7:
        return True

    h = len(pattern)
    for i, row in enumerate(pattern):
        for j, x in enumerate(row):
            if pattern[h - i - 1][j] == 1 and m[px + j, py + i] == "#":
                return True
    return False


def save_pattern(m, pattern, pattern_offset):
    px, py = pattern_offset
    h = len(pattern)
    for i, row in enumerate(pattern):
        for j, x in enumerate(row):
            p = pattern[h - i - 1][j]
            if p == 1:
                m[px + j, py + i] = "#"


def set_bit(x, n):
    return x | (1 << n)


def build_state(m, y_max):
    state = 0
    covered = 0
    w = 4
    for i in range(7):
        for j in range(w):
            if m[i, y_max - j] == "#":
                state = set_bit(state, i * w + j)
                covered = set_bit(covered, i)
    return state, covered


class RockSimulator:
    def __init__(self, m: SparseMap, jet_patterns):
        self.m = m
        self.rock_id = 0
        self.jet_id = 0
        self.jet_patterns = jet_patterns
        self.rock_spawned = 0

    def spawn_rock(self):
        _, (y_min, y_max) = self.m.limits()
        loc = 2, y_max + 4
        rock_pattern = ROCK_PATTERNS[self.rock_id]
        while True:
            sh_dir = self.jet_patterns[self.jet_id]
            self.jet_id = (self.jet_id + 1) % len(self.jet_patterns)
            if sh_dir == ">" and not collides(
                self.m, rock_pattern, (loc[0] + 1, loc[1])
            ):
                loc = loc[0] + 1, loc[1]
            elif sh_dir == "<" and not collides(
                self.m, rock_pattern, (loc[0] - 1, loc[1])
            ):
                loc = loc[0] - 1, loc[1]
            new_loc = loc[0], loc[1] - 1
            if collides(self.m, rock_pattern, new_loc):
                save_pattern(self.m, rock_pattern, loc)
                self.rock_id = (self.rock_id + 1) % len(ROCK_PATTERNS)
                self.rock_spawned += 1
                break
            else:
                loc = new_loc

    def jet_id_relative(self):
        return self.jet_id % len(self.jet_patterns)

    def loop_until_period(self):
        history = {}
        while True:
            y_max_current = self.y_max()
            state, covered = build_state(self.m, y_max_current)
            if covered == 127:
                key = state, self.jet_id_relative(), self.rock_id
                if key in history:
                    step_old, y_max_old = history[key]
                    return step_old, self.rock_spawned, y_max_old, y_max_current
                history[key] = self.rock_spawned, y_max_current
            self.spawn_rock()

    def y_max(self):
        return self.m.limits()[1][1]


def part_1(aoc_input):
    simulator = RockSimulator(SparseMap({}, default="."), aoc_input)
    for i in range(2022):
        simulator.spawn_rock()
    assert simulator.rock_spawned == 2022
    return simulator.y_max()


def part_2(aoc_input):
    # target = 2022
    target = 1000000000000

    simulator = RockSimulator(SparseMap({}, default="."), aoc_input)
    step_old, step, y_old, y_new = simulator.loop_until_period()

    delta = step - step_old
    delta_y = y_new - y_old
    height = y_old + ((target - step_old) // delta) * delta_y
    remaining = (target - step_old) % delta
    for i in range(remaining):
        simulator.spawn_rock()
    y_extra = simulator.y_max()

    return height + y_extra - y_new


def aoc_inputs():
    return {
        "example": ("day17-input-ex", 3068, 1514285714288),
        "real": ("day17-input-1", 3202, 1591977077352),
    }
