# Skeleton for days
import collections
import copy
import re

ACTION_RE = re.compile(r"move (\d+) from (\d+) to (\d+)")


def parse_input(raw: str):
    stacks = collections.defaultdict(list)
    lines = raw.splitlines()
    line_offset = 0
    for (li, l) in enumerate(lines):
        if l.startswith(" 1"):
            line_offset = li + 2
            break
        i = 0
        while i < len(l):
            if l[i] == "[":
                stack_idx = (i // 4) + 1
                stacks[stack_idx].append(l[i + 1])
                i += 3
            else:
                i += 1
    for s in stacks.values():
        s.reverse()
    actions = []
    for l in lines[line_offset:]:
        actions.append(tuple(map(int, ACTION_RE.match(l).groups())))
    return stacks, actions


def part_1(input):
    stack, actions = input
    stack = copy.deepcopy(stack)
    for rep, src, dst in actions:
        for _ in range(rep):
            if stack[src]:
                pass
            h = stack[src].pop()
            stack[dst].append(h)
    return "".join(stack[i + 1][-1] for i in range(len(stack)))


def part_2(input):
    stack, actions = input
    stack = copy.deepcopy(stack)
    for rep, src, dst in actions:
        tmp = []
        for _ in range(rep):
            if stack[src]:
                pass
            tmp.append(stack[src].pop())
        tmp.reverse()
        stack[dst].extend(tmp)
    return "".join(stack[i + 1][-1] for i in range(len(stack)))


def aoc_inputs():
    return {
        "example": ("day5-input-ex", "CMZ", "MCD"),
        "real": ("day5-input-1", "PTWLTDSJV", "WZMFVGGZP"),
    }
