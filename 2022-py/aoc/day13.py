from functools import cmp_to_key


def parse_input(raw: str):
    lines = raw.splitlines()
    pairs = []
    for i in range(0, len(lines), 3):
        l0 = eval(lines[i])
        l1 = eval(lines[i + 1])
        pairs.append((l0, l1))
    return pairs


def compare_int(x, y):
    if x == y:
        return 0
    elif x < y:
        return -1
    else:
        return 1


def compare(x, y):
    if isinstance(x, int) and isinstance(y, int):
        return compare_int(x, y)
    elif isinstance(x, list) and isinstance(y, list):
        for u, v in zip(x, y):
            d = compare(u, v)
            if d != 0:
                return d
        return compare_int(len(x), len(y))
    elif isinstance(y, int):
        return compare(x, [y])
    elif isinstance(x, int):
        return compare([x], y)
    else:
        assert False, "not handled"


def part_1(input):
    score = 0
    for i, (x, y) in enumerate(input):
        d = compare(x, y)
        if d == -1:
            score += i + 1
    return score


def part_2(lst):
    flat = []
    for x, y in lst:
        flat.append(x)
        flat.append(y)
    flat.extend([[[6]], [[2]]])
    scores_sorted = list(sorted(flat, key=cmp_to_key(compare)))
    acc = 1
    for i, elt in enumerate(scores_sorted):
        print(f"{i}: {elt}")
        if elt == [[6]]:
            acc *= i + 1
        if elt == [[2]]:
            acc *= i + 1
    return acc


def aoc_inputs():
    return {
        "example": ("day13-input-ex", 13, 140),
        "real": ("day13-input-1", 394, None),
    }
