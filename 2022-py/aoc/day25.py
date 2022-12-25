# Skeleton for days
import copy

VALUES = {
    "-": -1,
    "=": -2,
}


def decomp(x):
    parts = []
    while True:
        if x < 5:
            parts.append(x)
            return parts
        parts.append(x % 5)
        x = x // 5


def add_1(xs):
    xs = copy.deepcopy(xs)
    for i in range(len(xs)):
        if xs[i] <= 3:
            xs[i] += 1
            return xs
        else:
            xs[i] = 0
    xs.append(1)
    return xs


def normalize(xs):
    for i in range(len(xs)):
        if xs[i] >= 3:
            xs = xs[: i + 1] + add_1(xs[i + 1 :])
            xs[i] -= 5
    return xs


def encode(xs):
    chars = []
    for x in reversed(xs):
        if x == -1:
            chars.append("-")
        elif x == -2:
            chars.append("=")
        else:
            assert 0 <= x < 3
            chars.append(str(x))
    return "".join(chars)


def decode(s):
    values = []
    for c in s:
        if c == "-":
            values.append(-1)
        elif c == "=":
            values.append(-2)
        else:
            values.append(int(c))
    return list(reversed(values))


def as_int(xs):
    acc = 1
    total = 0
    for x in xs:
        total += acc * x
        acc *= 5
    return total


def parse_input(raw: str):
    numbers = []
    for line in raw.splitlines():
        numbers.append(decode(line))
    return numbers


def part_1(input):
    # print(input)
    total = 0
    for x in input:
        # print(f"{x} -> {as_int(x)}")
        total += as_int(x)
    # print("total:", total)
    # print()
    snafu_repr = encode(normalize(decomp(total)))
    return snafu_repr


def part_2(input):
    return 2 * len(input)


def aoc_inputs():
    return {
        "example": ("day25-input-ex", "2=-1=0", 8),
        "real": ("day25-input-1", "2==221=-002=0-02-000", None),
    }
