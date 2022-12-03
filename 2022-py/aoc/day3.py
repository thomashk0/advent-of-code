from aoc import chunks


def parse_input(raw: str):
    return raw.splitlines()


def char_score(c):
    c_ord = ord(c)
    if ord("a") <= c_ord <= ord("z"):
        return c_ord - ord("a") + 1
    if ord("A") <= c_ord <= ord("Z"):
        return c_ord - ord("A") + 27
    else:
        assert False


def score(s):
    mid = len(s) // 2
    s_left, s_right = s[:mid], s[mid:]
    common = set(s_left) & set(s_right)
    return sum(char_score(c) for c in common)


def part_1(input):
    s = [score(s) for s in input]
    return sum(s)


def score_2(chunk):
    common = set(chunk[0]) & set(chunk[1]) & set(chunk[2])
    return sum(char_score(c) for c in common)


def part_2(input):
    s = [score_2(s) for s in chunks(input, 3)]
    return sum(s)


def aoc_inputs():
    return {"example": ("day3-input-ex", 157, 70), "real": ("day3-input-1", 7848, 2616)}
