from pathlib import Path

import aoc

DAY = Path(__file__).name


class Input(aoc.AocInput):
    def __init__(self, lines):
        self.lines = lines

    @classmethod
    def from_path(cls, path):
        return cls(aoc.lines(path))


def part_1(input: Input):
    return None


def part_2(input: Input):
    return None


def aoc_solution():
    inputs = {
        "example": (f"{DAY}-input-ex", 1, 1),
        "real": (f"{DAY}-input-1", 23, 32),
    }
    return aoc.AocSolution(f"2022-{DAY}", Input, part_1, part_2), inputs


if __name__ == "__main__":
    aoc.aoc_run_solver(aoc_solution)
