import re

SPEC_RE = re.compile("(.*)\(contains(.*)\)")


def parse(lines):
    for line in lines:
        line = line.strip()
        if m := SPEC_RE.match(line):
            ingredients = set(m.group(1).split())
            allergens = set(x.strip() for x in m.group(2).split(','))
            yield ingredients, allergens
        else:
            raise ValueError("parse error")


def recover_allergens(input):
    remaining_allergens = set.union(*[x for _, x in input])
    known = {}
    while True:
        if len(remaining_allergens) == 0:
            return known
        for candidate in remaining_allergens:
            s = set.intersection(*[i for i, a in input if candidate in a])
            if len(s) == 1:
                value = next(iter(s))
                known[candidate] = value
                for i, a in input:
                    i.discard(value)
                    a.discard(candidate)
                remaining_allergens.discard(candidate)
                break


def aoc_run(input_path):
    import copy
    input = list(parse(open(input_path)))
    m = recover_allergens(copy.deepcopy(input))
    sane = set.union(*[x for x, _ in input]) - set(m.values())
    total = 0
    for i, _ in input:
        total += sum(x in sane for x in i)
    print("part 1:", total)
    bad = list(m.items())
    bad.sort(key=lambda x: x[0])
    print("part 2:", ",".join(x for _, x in bad))


if __name__ == '__main__':
    aoc_run('assets/day21-input-1')
