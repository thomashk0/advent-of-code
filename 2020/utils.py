"""A bunch of tools
"""


def transpose(l):
    """
    >>> transpose([[1, 2, 3], [4, 5, 6]])
    [[1, 4], [2, 5], [3, 6]]
    >>> transpose([[1, 4], [2, 5], [3, 6]])
    [[1, 2, 3], [4, 5, 6]]

    """
    return list(map(list, zip(*l)))


def parse(lines):
    active = set()
    for line_num, line in enumerate(lines):
        for col_num, char in enumerate(line.strip()):
            if char != '.':
                active.add((col_num, line_num, 0, 0))
    return active
