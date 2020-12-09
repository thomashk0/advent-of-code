import itertools


def is_valid(lines, i):
    all_sums = set(x + y for x, y in itertools.combinations(lines[i:25 + i], 2))
    current = lines[i + 25]
    if current not in all_sums:
        return True, current
    return False, current


def part_1(lines):
    for i in range(len(lines)):
        b, v = is_valid(lines, i)
        if b:
            return v


def part_2(lines, target):
    for i in range(len(lines)):
        tot = lines[i]
        for j in range(i + 1, len(lines)):
            tot += lines[j]
            if tot == target:
                return i, j
            if tot > target:
                break


def main():
    lines = list(map(int, open('assets/day9-input')))
    v = part_1(lines)
    print("part 1:", v)
    i, j = part_2(lines, v)
    rmin = min(lines[i: j + 1])
    rmax = max(lines[i: j + 1])
    print("part 2:", rmin + rmax)


if __name__ == '__main__':
    main()
