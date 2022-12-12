def parse_input(raw: str):
    level = {}
    start, end = None, None
    for i, line in enumerate(raw.splitlines()):
        for j, c in enumerate(line):
            height = ord(c)
            if c == "S":
                height = ord("a")
                start = i, j
            elif c == "E":
                height = ord("z")
                end = i, j
            level[i, j] = height - ord("a")

    return level, start, end


def around(p):
    px, py = p
    yield px + 1, py
    yield px - 1, py
    yield px, py + 1
    yield px, py - 1


def part_1(input):
    level, start, end = input
    to_explore = [start]
    explored = set()
    dist = 0
    # BFS search
    while True:
        to_explore_next = set()
        if not to_explore:
            print("warning: no solution found...")
            break
        for node in to_explore:
            explored.add(node)
            if node == end:
                return dist
            for child in around(node):
                if child not in explored and child in level:
                    if level[child] - level[node] <= 1:
                        to_explore_next.add(child)
        to_explore = list(to_explore_next)
        dist += 1


def part_2(input):
    level, start, end = input
    to_explore = [end]
    explored = {}
    dist = 0
    # BFS explore the full graph from the end
    while True:
        if not to_explore:
            break
        to_explore_next = set()
        for node in to_explore:
            explored[node] = dist
            for child in around(node):
                if child not in explored and child in level:
                    # The condition is inverted compared to part 1!
                    if level[node] - level[child] <= 1:
                        to_explore_next.add(child)
        to_explore = list(to_explore_next)
        dist += 1
    best = min(
        [(k, v) for k, v in explored.items() if level[k] == 0], key=lambda x: x[1]
    )
    return best[1]


def aoc_inputs():
    return {"example": ("day12-input-ex", 31, 29), "real": ("day12-input-1", 394, None)}
