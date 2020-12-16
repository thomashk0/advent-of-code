def parse(lines):
    return map(int, lines.split(','))


def solve(cmds, target):
    spoken = {n: k + 1 for k, n in enumerate(cmds[:-1])}
    last_spoken = cmds[-1]
    for round in range(len(cmds) + 1, target + 1):
        x = spoken.get(last_spoken)
        spoken[last_spoken] = round - 1
        if x is None:
            last_spoken = 0
        else:
            last_spoken = round - 1 - x
    return last_spoken


def aoc_run(input_path):
    import pathlib
    numbers = list(parse(pathlib.Path(input_path).read_text()))
    print("part 1:", solve(numbers, 2020))
    print("part 2:", solve(numbers, 30000000))


if __name__ == '__main__':
    aoc_run('assets/day15-input-1')
