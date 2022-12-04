from aoc import ints


def parse_input(raw: str):
    r = []
    for line in raw.splitlines():
        fst, snd = tuple(line.split(","))
        r.append((tuple(ints(fst, "-")), (tuple(ints(snd, "-")))))
    return r


def part_1(input):
    s = 0
    for (fst, snd) in input:
        if fst[0] <= snd[0] and fst[1] >= snd[1]:
            s += 1
        elif snd[0] <= fst[0] and snd[1] >= fst[1]:
            s += 1
    return s


def part_2(input):
    s = 0
    for (fst, snd) in input:
        distinct = fst[0] > snd[1] or snd[0] > fst[1]
        if not distinct:
            s += 1
    return s


def aoc_inputs():
    return {"example": ("day4-input-ex", 2, 4), "real": ("day4-input-1", 450, 837)}
