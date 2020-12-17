import itertools

DIRS_3D = list(itertools.product(*([[-1, 0, 1]] * 3 + [[0]])))
DIRS_4D = list(itertools.product(*([[-1, 0, 1]] * 4)))


def parse(lines):
    active = set()
    for line_num, line in enumerate(lines):
        for col_num, char in enumerate(line.strip()):
            if char != '.':
                active.add((col_num, line_num, 0, 0))
    return active


def neighbours(p, dirs):
    x, y, z, w = p
    for dx, dy, dz, dw in dirs:
        if dx == dy == dz == dw == 0:
            continue
        yield x + dx, y + dy, z + dz, w + dw


def step(m, dirs):
    new_state = set()
    explored = set()
    to_explore = set(m)
    while len(to_explore) > 0:
        x = to_explore.pop()
        if x in explored:
            continue
        explored.add(x)

        active_neighbours = sum(n in m for n in neighbours(x, dirs))
        if x not in m and active_neighbours == 3:
            new_state.add(x)
        elif x in m:
            to_explore.update(neighbours(x, dirs))
            if 2 <= active_neighbours <= 3:
                new_state.add(x)
            else:
                # Becomes inactive => do not insert the new state
                pass
    return new_state


def run(m, dirs, rounds=6):
    m = set(m)
    for i in range(rounds):
        m = step(m, dirs)
    return m


def aoc_run(input_path):
    m = parse(open(input_path))
    print("part 1:", len(run(m, DIRS_3D)))
    print("part 2:", len(run(m, DIRS_4D)))


if __name__ == '__main__':
    aoc_run('assets/day17-input-1')
