import abc
import importlib
import time
from pathlib import Path
from typing import Union


def lines(f: Union[str, Path], encoding=None):
    return Path(f).read_text(encoding=encoding).splitlines()


class AocInput(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def from_path(cls, path: Union[str, Path]):
        pass


class AocSolution:
    def __init__(self, day, input_cls: AocInput, part_1=None, part_2=None):
        self.day = day
        self.input_cls = input_cls
        self.part_1 = part_1
        self.part_2 = part_2

    def run(self, src, part_1_check=None, part_2_check=None, prefix="", verbose=True):
        t_parse = time.monotonic()
        input = self.input_cls.from_path(src)
        t_parse = time.monotonic() - t_parse
        prefix = f"[{self.day}.{prefix}] "
        print(f"{prefix}input loading (elapsed: {t_parse:.4f}s)")

        if self.part_1:
            t_part_1 = time.monotonic()
            part1_sol = self.part_1(input)
            t_part_1 = time.monotonic() - t_part_1
            if part_1_check is not None:
                assert part1_sol == part_1_check
            if verbose:
                print(f"{prefix}part 1: {part1_sol} (elapsed: {t_part_1:.4f}s)")

        if self.part_2:
            t_part_2 = time.monotonic()
            part2_sol = self.part_2(input)
            t_part_2 = time.monotonic() - t_part_2
            if part_2_check is not None:
                assert part2_sol == part_2_check
            if verbose:
                print(f"{prefix}part 2: {part2_sol} (elapsed: {t_part_2:.4f}s)")


def aoc_run_solver(solution):
    solver, inputs = solution()
    for k, (path, part_1_check, part_2_check) in inputs.items():
        solver.run(
            Path("assets") / path,
            part_1_check=part_1_check,
            part_2_check=part_2_check,
            prefix=k,
        )


def aoc_run(day):
    m = importlib.import_module(f"aoc.{day}")
    aoc_run_solver(m.aoc_solution())
