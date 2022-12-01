import aoc


def elf_weights(raw):
    parts = []
    acc = 0
    for part in raw:
        if part == "":
            parts.append(acc)
            acc = 0
        else:
            acc += int(part)
    parts.append(acc)
    return parts


class Input(aoc.AocInput):
    def __init__(self, lines):
        self.lines = lines
        self.weights = elf_weights(lines)

    @classmethod
    def from_path(cls, path):
        return cls(aoc.lines(path))


def part_1(input: Input):
    return max(input.weights)


def part_2(input: Input):
    weight_sorted = sorted(input.weights, reverse=True)
    return sum(weight_sorted[:3])


def aoc_solution():
    inputs = {
        "example": ("day1-input-ex", 24000, 45000),
        "real": ("day1-input-1", 69528, 206152),
    }
    return aoc.AocSolution("2022-day1", Input, part_1, part_2), inputs


if __name__ == "__main__":
    aoc.aoc_run_solver(aoc_solution)
