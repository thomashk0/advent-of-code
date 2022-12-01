from typing import Sequence


def parse_input(raw: str) -> Sequence[int]:
    parts = []
    acc = 0
    for part in raw.splitlines():
        if part == "":
            parts.append(acc)
            acc = 0
        else:
            acc += int(part)
    parts.append(acc)
    return parts


def part_1(input):
    return max(input)


def part_2(input):
    weight_sorted = sorted(input, reverse=True)
    return sum(weight_sorted[:3])


def aoc_inputs():
    return {
        "example": ("day1-input-ex", 24000, 45000),
        "real": ("day1-input-1", 69528, 206152),
    }
