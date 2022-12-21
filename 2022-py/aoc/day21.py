import copy
import re

from z3 import Solver, Real

DEF_RE = re.compile(r"(\w+): (\d+)")
MATH_RE = re.compile(r"(\w+): (\w+) ([+*/-]) (\w+)")


def parse_input(raw: str):
    ctx = {}
    for r in raw.splitlines():
        if v := DEF_RE.match(r):
            name, value = v.groups()
            ctx[name] = int(value)
        elif v := MATH_RE.match(r):
            name, src1, op, src2 = v.groups()
            ctx[name] = src1, op, src2
        else:
            raise ValueError(f"invalid line: {r}")
    return ctx


def eval_expr(ctx, target):
    v = ctx[target]
    if isinstance(v, int):
        return v
    src1, op, src2 = v
    x_1 = eval_expr(ctx, src1)
    x_2 = eval_expr(ctx, src2)
    if op == "+":
        r = x_1 + x_2
    elif op == "-":
        r = x_1 - x_2
    elif op == "/":
        r = x_1 // x_2
    elif op == "*":
        r = x_1 * x_2
    else:
        raise NotImplemented()
    ctx[target] = r
    return r


def part_1(ctx):
    ctx = copy.deepcopy(ctx)
    return eval_expr(ctx, "root")


def make_symbolic(ctx, target):
    v = ctx[target]

    if isinstance(v, tuple):
        src1, op, src2 = v
        x_1 = make_symbolic(ctx, src1)
        x_2 = make_symbolic(ctx, src2)
        if op == "+":
            r = x_1 + x_2
        elif op == "-":
            r = x_1 - x_2
        elif op == "/":
            r = x_1 / x_2
        elif op == "*":
            r = x_1 * x_2
        else:
            raise NotImplemented()
        ctx[target] = r
        return r
    else:
        return v


def part_2(ctx):
    humn = Real("x")
    ctx["humn"] = humn
    l, _, r = ctx["root"]
    l_expr = make_symbolic(ctx, l)
    r_expr = make_symbolic(ctx, r)
    eq = l_expr == r_expr
    solver = Solver()
    solver.add(eq)
    solver.check()
    m = solver.model()
    return m[humn].as_long()


def aoc_inputs():
    return {
        "example": ("day21-input-ex", 152, 301),
        "real": ("day21-input-1", 83056452926300, 3469704905529),
    }
