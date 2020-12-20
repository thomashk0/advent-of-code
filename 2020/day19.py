import copy
import re

LEAF_RE = re.compile(r"(\d+):\s*\"(\w)\"")
ID_RE = re.compile(r"(\d+):")


def parse(lines):
    rules = {}
    words = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if m := LEAF_RE.match(line):
            rules[int(m.group(1))] = m.group(2)
        elif m := ID_RE.match(line):
            line = ID_RE.sub('', line)
            parts = line.split('|')
            parts = [[int(x) for x in part.split()] for part in parts]
            rules[int(m.group(1))] = parts
        else:
            words.append(line)
    return rules, words


def expand_l(spec, rule):
    if len(rule) == 0:
        return []

    r_id = rule[0]
    if isinstance(r_id, str):
        return [rule]

    r_id = spec[rule[0]]
    if isinstance(r_id, str):
        return [[r_id] + rule[1:]]
    else:
        return [r_ids + rule[1:] for r_ids in r_id]


def expand_pass(spec, rs):
    new_l = []
    for r in rs:
        if len(r) == 0:
            continue
        new_l.extend(expand_l(spec, r))
    return new_l


def filter(candidates, w):
    for hyp in candidates:
        h0 = hyp[0]
        if isinstance(h0, str) and w[0] != h0:
            continue
        yield hyp


def matches_rules(rules, w):
    current = [[0]]
    while True:
        if len(w) == 0:
            return any(len(x) == 0 for x in current)

        if len(current) == 0:
            return False

        # Debug:
        # print("===")
        # print("state:", current)
        # print("w    :", w)
        # print()

        old = current
        current = expand_pass(rules, current)
        current = list(filter(current, w))

        if old == current:
            w = w[1:]
            current = [x[1:] for x in current]


def aoc_run(input_file):
    rules, words = parse(open(input_file))
    total = 0

    print("part 1:", sum(matches_rules(rules, w) for w in words))
    rules_m = copy.copy(rules)
    rules_m[11] = [[42, 31], [42, 11, 31]]
    rules_m[8] = [[42], [42, 8]]
    # for w in words:
    #     print(w, "->", matches_rules(rules_m, w))
    #     total += 1
    print("part 2:", sum(matches_rules(rules_m, w) for w in words))


if __name__ == '__main__':
    aoc_run('assets/day19-input-1')
