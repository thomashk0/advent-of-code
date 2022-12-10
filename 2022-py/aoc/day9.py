from collections import defaultdict

MOVES = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}


def parse_input(raw: str):
    input = []
    for line in raw.splitlines():
        d, cnt = line.split()
        input.append((d, MOVES[d], int(cnt)))
    return input


def is_adjacent(x, y):
    return abs(x[0] - y[0]) <= 1 and abs(x[1] - y[1]) <= 1


def clip(x, x_min, x_max):
    return max(min(x, x_max), x_min)


def diag(x, y):
    return clip(x[0] - y[0], -1, 1), clip(x[1] - y[1], -1, 1)


def part_1(input):
    # print(input)
    h_coords = (0, 0)
    t_coords = (0, 0)
    covered = defaultdict(int)
    for _, (dx, dy), cnt in input:
        for k in range(cnt):
            h_new = (h_coords[0] + dx, h_coords[1] + dy)
            if not is_adjacent(t_coords, h_new):
                t_coords = h_coords
            h_coords = h_new
            covered[t_coords] += 1
    return len(covered)


def align(head, tail):
    if is_adjacent(head, tail):
        return tail
    d = diag(head, tail)
    return tail[0] + d[0], tail[1] + d[1]


def part_2(input):
    parts = 10
    snake = [(0, 0) for _ in range(parts)]
    covered = defaultdict(int)
    for _, (dx, dy), cnt in input:
        for k in range(cnt):
            # move the head
            snake[0] = (snake[0][0] + dx, snake[0][1] + dy)
            for i in range(1, len(snake)):
                if is_adjacent(snake[i], snake[i - 1]):
                    break
                snake[i] = align(snake[i - 1], snake[i])
            covered[snake[-1]] += 1
    return len(covered)


def aoc_inputs():
    return {
        "example": ("day9-input-ex", 13, 1),
        "example-2": ("day9-input-ex-2", None, 36),
        "real": ("day9-input-1", 6026, 2273),
    }
