import copy
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Sequence

import aoc


@dataclass
class Monkey:
    items: list
    op: str
    op_arg: int
    test: (int, int, int)

    def update_worry(self, old: int) -> int:
        op_arg = old if self.op_arg == "old" else int(self.op_arg)
        if self.op == "+":
            return old + op_arg
        elif self.op == "*":
            return old * op_arg

    def test_worry(self, value: int) -> int:
        if value % self.test[0] == 0:
            return self.test[1]
        else:
            return self.test[2]


def parse_input(raw: str):
    lines = raw.splitlines()
    monkeys = []
    for i in range(0, len(lines), 7):
        items = [int(x) for x in lines[i + 1].split(":")[1].split(",")]
        op = re.search(r"new = old ([+*]) (old|\d+)", lines[i + 2])
        op, op_arg = tuple(op.groups())
        test_val = re.search(r"divisible by (\d+)", lines[i + 3]).groups()[0]
        test_true = re.search(r"throw to monkey (\d+)", lines[i + 4]).groups()[0]
        test_false = re.search(r"throw to monkey (\d+)", lines[i + 5]).groups()[0]
        monkeys.append(
            Monkey(
                items=items,
                op=op,
                op_arg=op_arg,
                test=(int(test_val), int(test_true), int(test_false)),
            )
        )
    return monkeys


def turn(monkeys: Sequence[Monkey], items_inspected, div_reduce=None, mod_reduce=None):
    for i in range(len(monkeys)):
        m = monkeys[i]
        items = m.items
        m.items = []
        items_inspected[i] += len(items)
        for it in items:
            new_value = m.update_worry(it)
            if div_reduce:
                new_value = new_value // 3
            if mod_reduce:
                new_value = new_value % mod_reduce
            target = m.test_worry(new_value)
            monkeys[target].items.append(new_value)


def part_1(input):
    monkeys = copy.deepcopy(input)
    items_inspected = defaultdict(int)
    for i in range(20):
        turn(monkeys, items_inspected, div_reduce=3)
    print(items_inspected)
    best = sorted(list(items_inspected.items()), key=lambda x: x[1], reverse=True)
    return best[0][1] * best[1][1]


def part_2(input):
    ppcm = aoc.prod([m.test[0] for m in input])
    items_inspected = defaultdict(int)
    for i in range(10000):
        turn(input, items_inspected, mod_reduce=ppcm)
    best = sorted(list(items_inspected.items()), key=lambda x: x[1], reverse=True)
    return best[0][1] * best[1][1]


def aoc_inputs():
    return {
        "example": ("day11-input-ex", 10605, 2713310158),
        "real": ("day11-input-1", 62491, 8),
    }
