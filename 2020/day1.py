import itertools


def main():
    lines = list(map(int, open('assets/day1-input')))
    for i, k in itertools.product(lines, lines):
        if i + k == 2020:
            print("part 1:", i * k)
            break

    for i, k, l in itertools.product(lines, lines, lines):
        if i + k + l == 2020:
            print("part 2:", i * k * l)
            return


if __name__ == '__main__':
    main()
