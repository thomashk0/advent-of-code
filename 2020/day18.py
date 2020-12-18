import itertools
from pyparsing import Word, nums, oneOf, Forward, Suppress, Group

EXPR = Forward()
INTEGER = Word(nums)
OPERATOR = oneOf('+ *')
lpar, rpar = Suppress('('), Suppress(')')
PEXPR = lpar + EXPR + rpar
EXPR <<= INTEGER + OPERATOR + EXPR \
         | Group(PEXPR) + OPERATOR + EXPR \
         | Group(PEXPR) \
         | INTEGER


class Sum:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f'Sum({self.data})'


def parse(lines, parser=EXPR):
    for line in lines:
        yield parser.parseString(line.strip()).asList()


def eval_op(op, x, y):
    if op == '+':
        return x + y
    elif op == '*':
        return x * y
    else:
        raise NotImplementedError()


def reduce_expr(expr):
    if isinstance(expr, int):
        return expr
    elif len(expr) == 1:
        return int(expr[0])
    x, op, y = expr[:3]
    x = int(x) if isinstance(x, str) else reduce_expr(x)
    y = int(y) if isinstance(y, str) else reduce_expr(y)
    t = eval_op(op, x, y)
    return reduce_expr([t] + expr[3:])


def remove_add_node(p):
    return [x for x in p if x != '+']


def make_product_tree(expr):
    acc = []
    l = []
    for e in itertools.chain(expr, ['*']):
        if e == '*':
            acc.append(Sum(remove_add_node(l)))
            l = []
            continue
        child = e
        if isinstance(e, list):
            child = make_product_tree(e)
        l.append(child)
    return acc


def reduce_expr_alt(expr):
    if isinstance(expr, Sum):
        return sum(reduce_expr_alt(e) for e in expr.data)
    elif isinstance(expr, str):
        return int(expr)
    else:
        acc = 1
        for e in expr:
            acc *= reduce_expr_alt(e)
        return acc


def aoc_run(input_path):
    exprs = list(parse(open(input_path)))
    print("part 1:", sum(reduce_expr(e) for e in exprs))
    print("part 2:", sum(reduce_expr_alt(make_product_tree(e)) for e in exprs))


def test_parsing():
    def eval_part1(s):
        return reduce_expr(EXPR.parseString(s))

    assert eval_part1("1 + 2 * 3 + 4 * 5 + 6") == 71
    assert eval_part1("1 + (2 * 3) + (4 * (5 + 6))") == 51
    assert eval_part1(
        "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632

    def eval_part2(s):
        e = EXPR.parseString(s).asList()
        e = make_product_tree(e)
        return reduce_expr_alt(e)

    assert eval_part2("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060


if __name__ == '__main__':
    aoc_run('assets/day18-input-1')
