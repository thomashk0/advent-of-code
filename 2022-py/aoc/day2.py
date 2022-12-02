POINTS = {"A": 1, "B": 2, "C": 3}  # rock, paper, chisel
RENAME = {"X": "A", "Y": "B", "Z": "C"}
WIN_AGAINST = {"A": "C", "C": "B", "B": "A"}
LOOSE_AGAINST = {"C": "A", "B": "C", "A": "B"}


def parse_input(raw: str):
    return [r.split() for r in raw.splitlines()]


def outcome(a_choice, b_choice):
    s = POINTS[a_choice]
    if a_choice == b_choice:
        return s + 3
    elif WIN_AGAINST[a_choice] == b_choice:
        return s + 6
    else:
        return s


def part_1(input):
    input = [(c[0], RENAME[c[1]]) for c in input]
    return sum([outcome(y, x) for x, y in input])


def find_choice(x, y):
    if y == "Y":
        return x
    elif y == "X":
        return WIN_AGAINST[x]
    else:
        return LOOSE_AGAINST[x]


def part_2(input):
    return sum([outcome(find_choice(x, y), x) for x, y in input])


def aoc_inputs():
    return {
        "example": ("day2-input-ex", 15, 12),
        "real": ("day2-input-1", 9759, 12429),
    }
