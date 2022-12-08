import numpy as np


def parse_input(raw: str):
    m = [list(map(int, row)) for row in raw.splitlines()]
    return np.array(m, dtype=np.int32)


def is_visible(m, i, j):
    cur = m[i, j]
    r = (
        np.all(m[:i, j] < cur)
        or np.all(m[i + 1 :, j] < cur)
        or np.all(m[i, :j] < cur)
        or np.all(m[i, j + 1 :] < cur)
    )
    return r


def part_1(input):
    w, h = input.shape
    edges = w * h - (w - 2) * (h - 2)
    inner_visible = 0
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            inner_visible += int(is_visible(input, i, j))
    return edges + inner_visible


def viewing_distance(xs, cur):
    score = 0
    for ii in xs:
        if ii >= cur:
            return score + 1
        score += 1
    return score


def scenic_score(m: np.ndarray, i, j):
    cur = m[i, j]
    total = 1
    total *= viewing_distance(m[:i, j][::-1], cur)
    total *= viewing_distance(m[i + 1 :, j], cur)
    total *= viewing_distance(m[i, :j][::-1], cur)
    total *= viewing_distance(m[i, j + 1 :], cur)
    return total


def part_2(input):
    # print("score:", scenic_score(input, 1, 2))
    # print("score:", scenic_score(input, 3, 2))
    w, h = input.shape
    scores = np.zeros_like(input, dtype=np.int64)
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            s = scenic_score(input, i, j)
            assert s < 2**63
            scores[i, j] = s
            # inner_visible += int(is_visible(input, i, j))
    return np.max(scores)


def aoc_inputs():
    return {
        "example": ("day8-input-ex", 21, 8),
        "real": (
            "day8-input-1",
            1662,
            537600,
        ),  # 1443 is too low, p2, 1108800 is toohigh
    }
