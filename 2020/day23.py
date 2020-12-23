import itertools
import array

def make_circle(elts):
    succ = array.array('I')
    succ.fromlist([0] * (max(elts) + 1))
    for p, n in zip(elts, itertools.chain(elts[1:], (elts[0],))):
        succ[p] = n
    return succ


def find_destination_cup(circle, value, max_elem):
    while True:
        if circle[value]:
            return value
        value -= 1
        if value < 0:
            value = max_elem


def show_circle(circle, start, count=0, sep=' '):
    s = []
    n = start
    limit = len(circle)
    if count:
        limit = min(count, limit)
    for i in range(limit):
        s.append(str(n))
        n = circle[n]
    return sep.join(s)


def step(start, circle, max_elem):
    # print("cups:", show_circle(circle, start))
    n = start
    picked = []
    for i in range(3):
        n = circle[n]
        picked.append(n)
    circle[start] = circle[n]
    for k in picked:
        circle[k] = 0
    # print("pick up:", picked)

    n = find_destination_cup(circle, start - 1, max_elem)
    # print("destination:", n)
    # print()
    n_next = circle[n]
    for v in picked:
        circle[n] = v
        n = v
    circle[n] = n_next
    return circle[start]


def simulate(start, circle, rounds):
    max_elem = max(circle)
    for i in range(rounds):
        new_start = step(start, circle, max_elem)
        start = new_start


def solve(state, rounds):
    circle = make_circle(state)
    simulate(state[0], circle, rounds)
    return circle


def aoc_run(input_path):
    import time
    state = next(open(input_path))
    state = list(map(int, state.strip()))

    start = time.monotonic()
    circle = solve(state, 100)
    p1_elapsed = time.monotonic() - start
    print("part 1:", show_circle(circle, circle[1], sep='', count=8))

    p2_input = state + list(range(max(state) + 1, 1000001))
    start = time.monotonic()
    circle = solve(p2_input, 10 * 1000 * 1000)
    p2_elapsed = time.monotonic() - start
    x = circle[1]
    y = circle[x]
    print("part 2:", x * y)

    print()
    print("elapsed (part 1): ", p1_elapsed)
    print("elapsed (part 2): ", p2_elapsed)


if __name__ == '__main__':
    aoc_run('assets/day23-input-1')
