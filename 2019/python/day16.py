import itertools


def parse_input(s: str):
    return list(map(int, list(s.strip())))


def flatten(xs):
    return list(itertools.chain.from_iterable(xs))


def skip_first(it):
    next(it)
    return it


def dotp(xs, patt):
    # print(" + ".join(
    #     f"{x} * {y}" for x, y in zip(xs, skip_first(itertools.cycle(patt)))))
    r = sum(x * y for x, y in zip(xs, patt))
    return abs(r) % 10


def patterns(n, base_pattern):
    ps = [flatten([[x] * i for x in base_pattern]) for i in range(1, n + 1)]
    return [
        list(itertools.islice(skip_first(itertools.cycle(p)), n)) for p in ps]


def dump_patterns(n, base_pattern):
    for i, p in enumerate(patterns(n, base_pattern)):
        print(f"{i:2}", "".join(map(str, p)))


def fft_step(xs, patterns):
    return [dotp(xs, pat) for pat in patterns]


def fft_run(xs, phases, base_pattern):
    ps = patterns(len(xs), base_pattern)
    for i in range(phases):
        xs = fft_step(xs, ps)
        # print(f"After {i + 1} steps", xs)
    return xs


def part_1(*args):
    return "".join(str(x) for x in fft_run(*args)[:8])


def compute(r, xs, offset, phases):
    n = len(xs)
    xs = list(itertools.islice(itertools.cycle(xs), r * n))[offset:]
    # print(xs)
    ys = [0] * len(xs)
    for _ in range(phases):
        # Phase
        ys[0] = sum(xs)
        for i in range(1, len(xs)):
            ys[i] = ys[i - 1] - xs[i - 1]
        for i in range(len(ys)):
            ys[i] = abs(ys[i]) % 10
        xs, ys = ys, xs
    return xs


def part_2():
    base_pattern = [0, 1, 0, -1]
    s = open("assets/day16-input").readline().strip()
    i = parse_input(s)
    offset = int(s[:7])
    return compute(10000, i, offset, 100)
    # print("Offset is =>", offset)
    # print("Len =>", len(i))
    # print("len / offset => ", offset / (10000 * len(i)))
    # print("len - offset", 10000 * len(i) - offset)


def main():
    dump_patterns(8, [0, 1, 2, 3])
    base_pattern = [0, 1, 0, -1]
    i = parse_input("1234567812345678")
    print("f =", fft_run(i, 100, base_pattern)[9:])
    print("c =", compute(2, i[:8], 9, 100))

    assert part_1(parse_input("12345678"), 4, base_pattern) == "01029498"
    assert part_1(parse_input("80871224585914546619083218645595"), 100,
                   base_pattern) == "24176176"

    print("part 1:",
          part_1(parse_input(open("assets/day16-input").readline()), 100,
                  base_pattern))
    # 78009100
    print("part 2:", "".join(str(x) for x in part_2()[:8]))


if __name__ == '__main__':
    main()
