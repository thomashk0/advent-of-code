def parse_input(raw: str):
    cubes = [tuple(map(int, l.split(","))) for l in raw.splitlines()]
    return {c: "#" for c in cubes}


def visible_edges(world, air_bubbles):
    total = 6 * len(world)
    for cube in world:
        for c_around in around(cube):
            if c_around in world or c_around in air_bubbles:
                total -= 1
    return total


def part_1(cubes):
    return visible_edges(cubes, set())


def limits(world, margin=0):
    xs = [x for x, _, _ in world]
    ys = [y for _, y, _ in world]
    zs = [z for _, _, z in world]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    zmin, zmax = min(zs), max(zs)
    return (
        (xmin - margin, xmax + margin),
        (ymin - margin, ymax + margin),
        (zmin - margin, zmax + margin),
    )


AROUND = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1)]


def around(p):
    x, y, z = p
    for dx, dy, dz in AROUND:
        yield x + dx, y + dy, z + dz


def in_bounds(bounds, coords):
    for (vmin, vmax), v in zip(bounds, coords):
        if v < vmin or v > vmax:
            return False
    return True


def spread_air(world, air_bubbles, bounds, src):
    to_explore = {src}
    explored = set()
    cur = set()
    while len(to_explore) > 0:
        # if to_explore == ""
        p = to_explore.pop()
        if not in_bounds(bounds, p):
            # We reached the outer boundaries. This is not
            # a closed area.
            return
        explored.add(p)
        if p not in world:
            cur.add(p)
        for p_next in around(p):
            if p_next in explored or p_next in world:
                continue
            to_explore.add(p_next)

    for c in cur:
        air_bubbles.add(c)


def viz(world, air_bubbles):
    """
    Funny 3D visualization.
    """
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    xs, ys, zs = [], [], []
    for x, y, z in world.keys():
        xs.append(x)
        ys.append(y)
        zs.append(z)
    ax.scatter(xs, ys, zs, color="r", marker="s", s=100)
    xs, ys, zs = [], [], []
    for x, y, z in air_bubbles:
        xs.append(x)
        ys.append(y)
        zs.append(z)
    ax.scatter(xs, ys, zs, color="b", marker="s", s=100)
    plt.show()


def part_2(world):
    bounds = limits(world, margin=0)
    poi = set()
    for c in world:
        for c_next in around(c):
            if c_next not in world and in_bounds(bounds, c_next):
                poi.add(c_next)
    air_bubbles = set()
    for c in poi:
        spread_air(world, air_bubbles, bounds, c)

    # Sanity checks:
    assert len(air_bubbles.intersection(set(world.keys()))) == 0
    for c in air_bubbles:
        assert in_bounds(bounds, c)

    # viz(world, air_bubbles)

    return visible_edges(world, air_bubbles)


def aoc_inputs():
    return {
        "example": ("day18-input-ex", 64, 58),
        "real": ("day18-input-1", 4244, 2460),
    }
