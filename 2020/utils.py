"""A bunch of tools
"""

import re
from typing import List, Iterable


def lmap(f, *iterables):
    return list(map(f, *iterables))


def parse_ints(s: str) -> List[int]:
    return lmap(int, re.findall(r"-?\d+", s))


def parse_pos_ints(s: str) -> List[int]:
    return lmap(int, re.findall(r"\d+", s))


def parse_words(s: str):
    return re.findall(r"[a-zA-Z]+", s)


def parse_sparse_map(lines: Iterable[str], ignore='.'):
    active = set()
    for line_num, line in enumerate(lines):
        for col_num, char in enumerate(line.strip()):
            if char not in ignore:
                active.add((col_num, line_num))
    return active


# List operations

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


def prod(xs):
    acc = 1
    for x in xs:
        acc *= x
    return acc
