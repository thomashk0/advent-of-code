import re

LINE_RE = re.compile(r"(\d+)-(\d+) (\w): (\w+)")


def aoc_run(filename='assets/day2-input'):
    n_good = 0
    spec = []
    for line in open(filename):
        m = LINE_RE.match(line.strip())
        start, end, char, password = m.groups()
        start, end = int(start), int(end)
        spec.append((start, end, char, password))

    for start, end, char, password in spec:
        n_char = password.count(char)
        if start <= n_char <= end:
            n_good += 1
    print("part 1:", n_good)

    n_good = 0
    for start, end, char, password in spec:
        n_match = int(password[start - 1] == char)
        n_match += int(password[end - 1] == char)
        if n_match == 1:
            n_good += 1
    print("part 2:", n_good)


if __name__ == '__main__':
    aoc_run()
