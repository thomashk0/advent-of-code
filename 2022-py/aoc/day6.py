import aoc


def parse_input(raw: str):
    return raw.strip()


def part_1(input):
    for i in range(4, len(input)):
        if len(set(input[i - 4 : i])) == 4:
            return i
    assert False, "invalid"


def part_2(input):
    for i in range(14, len(input)):
        if len(set(input[i - 14 : i])) == 14:
            return i
    assert False


def aoc_inputs():
    return {
        "example-0": ("day6-input-ex", 7, 19),
        "example-1": (aoc.Str("bvwbjplbgvbhsrlpgdmjqwftvncz"), 5, 23),
        "example-2": (aoc.Str("nppdvjthqldpwncqszvftbrmjlhg"), 6, 23),
        "example-3": (aoc.Str("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"), 10, 29),
        "example-4": (aoc.Str("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"), 11, 26),
        "real": ("day6-input-1", None, None),
    }
