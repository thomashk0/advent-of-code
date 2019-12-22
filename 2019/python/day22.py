import itertools
from enum import Enum
from typing import NamedTuple, Optional
import re


class ActionKind(Enum):
    STACK = 0
    CUT = 1
    INCREMENT = 2


class Action(NamedTuple):
    kind: ActionKind
    arg: Optional[int] = None


def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def mod_inv(a, b):
    """return x such that (x * a) % b == 1"""
    g, x, _ = xgcd(a, b)
    if g == 1:
        return x % b


def symbolic_shuffle(action, s, n):
    k = action.kind
    # NOTE: position = (a * i + b) % n
    (a, b) = s
    if k == ActionKind.STACK:
        r = (-a, -b - 1)
    elif k == ActionKind.INCREMENT:
        r = (a * action.arg, b * action.arg)
    elif k == ActionKind.CUT:
        r = (a, b - action.arg)
    else:
        raise ValueError(f"unsupported action: {k}")
    return r[0] % n, r[1] % n


def repeat(coeffs, p, n):
    a, b = coeffs
    a_n = pow(a, p, n)
    a_inv = mod_inv((a - 1) % n, n)
    assert (a_inv * (a - 1) % n) % n == 1
    return a_n, (b * (a_n - 1) * a_inv) % n


def symbolic_shuffle_all(actions, n):
    s = (1, 0)
    for a in actions:
        s = symbolic_shuffle(a, s, n)
    return s


def parse_actions(s):
    actions = []
    for line in s:
        r = re.match(r"deal with increment (\d+)", line)
        if r:
            actions.append(Action(ActionKind.INCREMENT, int(r.group(1))))
            continue
        r = re.match(r"cut ([-]?\d+)", line)
        if r:
            actions.append(Action(ActionKind.CUT, int(r.group(1))))
            continue
        if re.match(r"deal into new stack", line):
            actions.append(Action(ActionKind.STACK))
            continue
        raise ValueError(f"parse error: {line}")
    return actions


def from_file(f_name):
    with open(f_name) as f:
        return parse_actions(f)


def part_2(actions):
    n = 119315717514047
    repeats = 101741582076661
    a, b = symbolic_shuffle_all(actions, n)
    a_f, b_f = repeat((a, b), repeats, n)
    a_f_inv = mod_inv(a_f, n)
    return ((2020 - b_f) * a_f_inv) % n


def part_1(actions):
    n = 10007
    a, b = symbolic_shuffle_all(actions, n)
    return (a * 2019 + b) % n


def main():
    actions = from_file("assets/day22-input")
    p1 = part_1(actions)
    assert p1 == 7395
    print("part 1:", p1)
    print("part 2:", part_2(actions))


if __name__ == '__main__':
    main()
