import importlib
import time
import re
from pathlib import Path
from typing import Union, List, Iterable

import numba


def ints(s: str, sep=" "):
    return map(int, s.split(sep))


def lines(f: Union[str, Path], encoding=None):
    return Path(f).read_text(encoding=encoding).splitlines()


def lmap(f, *iterables):
    return list(map(f, *iterables))


def parse_ints(s: str) -> List[int]:
    return lmap(int, re.findall(r"-?\d+", s))


def parse_pos_ints(s: str) -> List[int]:
    return lmap(int, re.findall(r"\d+", s))


def parse_words(s: str):
    return re.findall(r"[a-zA-Z]+", s)


def parse_sparse_map(lines: Iterable[str], ignore="."):
    active = set()
    for line_num, line in enumerate(lines):
        for col_num, char in enumerate(line.strip()):
            if char not in ignore:
                active.add((col_num, line_num))
    return active


def flatten(l):
    return [i for x in l for i in x]


def transpose(l):
    """
    >>> transpose([[1, 2, 3], [4, 5, 6]])
    [[1, 4], [2, 5], [3, 6]]
    >>> transpose([[1, 4], [2, 5], [3, 6]])
    [[1, 2, 3], [4, 5, 6]]

    """
    return list(map(list, zip(*l)))


def fst(x):
    return x[0]


def snd(x):
    return x[1]


@numba.njit()
def prod(xs):
    acc = 1
    for x in xs:
        acc *= x
    return acc


def chunks(seq, size):
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


C_RED = "\033[31m"
C_GREEN = "\033[32m"
C_ENDCOLOR = "\033[0m"


class AocRunner:
    def __init__(self, day, parse_input, part_1=None, part_2=None):
        self.day = day
        self.parse_input = parse_input
        self.part_1 = part_1
        self.part_2 = part_2

    def run(self, src, part_1_check=None, part_2_check=None, prefix="", verbose=True):
        t_parse = time.monotonic()
        input = self.parse_input(Path(src).read_text())
        t_parse = time.monotonic() - t_parse
        prefix = f"[{self.day}.{prefix}] "
        print(f"{prefix}input loading (elapsed: {t_parse:.4f}s)")

        if self.part_1:
            t_part_1 = time.monotonic()
            part1_sol = self.part_1(input)
            t_part_1 = time.monotonic() - t_part_1
            err_status = ""
            if part_1_check is not None and part1_sol != part_1_check:
                err_status = f", {C_RED}expected: {part_1_check}{C_ENDCOLOR}"
            if verbose:
                print(
                    f"{prefix}part 1: {part1_sol}{err_status} (elapsed: {t_part_1:.4f}s)"
                )

        if self.part_2:
            t_part_2 = time.monotonic()
            part2_sol = self.part_2(input)
            t_part_2 = time.monotonic() - t_part_2
            err_status = ""
            if part_2_check is not None and part2_sol != part_2_check:
                err_status = f", {C_RED}expected: {part_2_check}{C_ENDCOLOR}"
            if verbose:
                print(
                    f"{prefix}part 2: {part2_sol}{err_status} (elapsed: {t_part_2:.4f}s)"
                )


def _load_module(day, m):
    return AocRunner(day, m.parse_input, m.part_1, m.part_2), m.aoc_inputs()


def aoc_run(day):
    m = importlib.import_module(f"aoc.{day}")
    runner, tests = _load_module(day, m)
    for k, (path, part_1_check, part_2_check) in tests.items():
        runner.run(
            Path("assets") / path,
            part_1_check=part_1_check,
            part_2_check=part_2_check,
            prefix=k,
        )
