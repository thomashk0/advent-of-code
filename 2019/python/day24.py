import collections

import utils


def shape(m):
    (xmin, xmax), (ymin, ymax) = m.limits()
    center = (xmax - xmin) // 2, (ymax - ymin) // 2
    corners_from = {
        'R': [(xmin, i) for i in range(ymin, ymax + 1)],
        'L': [(xmax, i) for i in range(ymin, ymax + 1)],
        'S': [(i, ymin) for i in range(xmin, xmax + 1)],
        'N': [(i, ymax) for i in range(xmin, xmax + 1)]
    }
    return center, corners_from


def rating(m, limits):
    base = 1
    score = 0
    (xmin, xmax), (ymin, ymax) = limits
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            if m.get((0, (x, y))) == '#':
                score += base
            base *= 2
    return score


def part_1(m):
    limits = m.limits()
    (xmin, xmax), (ymin, ymax) = limits
    state = {(0, c): v for c, v in m.items()}

    def adjacents(_, p):
        for _, n in utils.neighbours(p):
            nx, ny = n
            if xmin <= nx <= xmax and ymin <= ny <= ymax:
                yield 0, n

    seen = {rating(state, limits)}
    while True:
        update_alt(state, adjacents)
        r = rating(state, limits)
        if r in seen:
            return r
        seen.add(r)


def update_alt(state, get_adjacent):
    # Find tiles to expand => all (recursive) neighbours of '#'
    extra_coords = set()
    for (level, p), v in state.items():
        if v == '#':
            for r in get_adjacent(level, p):
                if r not in state:
                    extra_coords.add(r)
    for r in extra_coords:
        state[r] = '.'

    # Count stuff around
    counts = collections.defaultdict(int)
    for loc, _ in state.items():
        level, p = loc
        for r in get_adjacent(level, p):
            if state.get(r) == '#':
                counts[loc] += 1

    for loc, val in state.items():
        cnt = counts[loc]
        val = state.get(loc, '.')
        if val == '#' and cnt != 1:
            state[loc] = '.'
        elif val == '.' and (cnt == 2 or cnt == 1):
            state[loc] = '#'
        else:
            state[loc] = val


def part_2(m):
    (xmin, xmax), (ymin, ymax) = m.limits()
    center, corners = shape(m)
    cx, cy = center
    state = {(0, (x, y)): v for (x, y), v in m.items()}

    def adjacents(level, p):
        coords = []
        for d, n in utils.neighbours(p):
            nx, ny = n
            if n == center:
                coords.extend(((level - 1), c) for c in corners[d])
                continue
            if nx < xmin:
                coords.append((level + 1, (cx - 1, cy)))
            elif nx > xmax:
                coords.append((level + 1, (cx + 1, cy)))
            if ny < ymin:
                coords.append((level + 1, (cx, cy - 1)))
            elif ny > ymax:
                coords.append((level + 1, (cx, cy + 1)))
            if xmin <= nx <= xmax and ymin <= ny <= ymax:
                coords.append((level, (nx, ny)))
        return coords

    for i in range(200):
        update_alt(state, adjacents)

    return collections.Counter(state.values())['#']


def main():
    m = utils.SparseMap.from_file("assets/day24-input")
    r = part_1(m)
    print("part 1:", r)
    print("part 2:", part_2(m))


if __name__ == "__main__":
    main()
