import itertools


def aoc_run(filename='assets/day1-input'):
    lines = list(map(int, open(filename)))
    for i, k in itertools.product(lines, lines):
        if i + k == 2020:
            print("part 1:", i * k)
            break

    for i, k, l in itertools.product(lines, lines, lines):
        if i + k + l == 2020:
            print("part 2:", i * k * l)
            return


if __name__ == '__main__':
    aoc_run()
