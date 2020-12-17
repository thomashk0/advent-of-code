import re
import itertools

LINE_RE = re.compile(r"([a-zA-Z ]+): (\d+)-(\d+) or (\d+)-(\d+)")


def parse_spec(lines):
    spec = []
    for i, l in enumerate(lines):
        if not l.strip():
            return lines[i + 1:], spec
        m = LINE_RE.match(l)
        label, a_low, a_high, b_low, b_high = m.groups()
        spec.append(
            (label, (int(a_low), int(a_high)), ((int(b_low), int(b_high)))))


def parse_tickets(lines):
    tickets = []
    for i, l in enumerate(lines):
        if not l.strip():
            return lines[i + 1:], tickets
        tickets.append(list(map(int, l.strip().split(','))))
    return [], tickets


def field_valid(field_spec, f):
    _, (al, ah), (bl, bh) = field_spec
    return (al <= f <= ah) or (bl <= f <= bh)


def all_fields_invalid(spec, f):
    return all(not field_valid(field, f) for field in spec)


def invalid_indices(spec, f):
    return (i for i, s in enumerate(spec) if not field_valid(s, f))


def parse(lines):
    lines, spec = parse_spec(lines)
    lines = lines[1:]
    lines, yours = parse_tickets(lines)
    lines = lines[1:]
    lines, nearby = parse_tickets(lines)
    return spec, yours, nearby


def part_1(spec, nearby):
    all_invalid = [v for v in itertools.chain.from_iterable(nearby) if
                   all_fields_invalid(spec, v)]
    return sum(all_invalid)


def remove_value(cols, i, value):
    remove_next = []
    for j, c in enumerate(cols):
        if j != i:
            if len(c) == 1:
                continue
            c.discard(value)
            if len(c) == 1:
                remove_next.append((j, next(iter(c))))
    for j, v in remove_next:
        remove_value(cols, j, v)


def check(spec, col, values):
    for k, row in enumerate(values):
        elt = row[col]
        if not field_valid(spec, row[col]):
            print(f"k = {k:4} => invalid field {elt}, {spec}")
        assert field_valid(spec, row[col])


def filter(elements):
    for i in range(len(elements)):
        col = elements[i]
        if len(col) == 1:
            remove_value(elements, i, next(iter(col)))


def part_2_alt(spec, yours, nearby):
    all_tickets = yours + nearby
    valid_rows = []
    for row in all_tickets:
        is_invalid = any(all_fields_invalid(spec, f) for f in row)
        if is_invalid:
            continue
        valid_rows.append(row)
    # print("row removed:", len(all_tickets) - len(valid_rows))
    n_cols = len(spec)
    possible_cols = []
    for s in spec:
        valid = set()
        for i in range(n_cols):
            vals = [row[i] for row in valid_rows]
            is_valid = all(field_valid(s, x) for x in vals)
            if is_valid:
                valid.add(i)
        possible_cols.append(valid)
    filter(possible_cols)
    cols = [next(iter(c)) for c in possible_cols]

    # Sanity check
    for s, v in zip(spec, cols):
        check(s, v, valid_rows)

    res = 1
    for s, value in zip(spec, cols):
        name, _, _ = s
        # print(f"{name:10} -> {yours[0][value]}")
        if name.startswith("departure"):
            res *= yours[0][value]
    return res


def aoc_run(input_path):
    spec, yours, nearby = list(parse(list(open(input_path))))
    print("part 1:", part_1(spec, nearby))
    print("part 2:", part_2_alt(spec, yours, nearby))


if __name__ == '__main__':
    aoc_run('assets/day16-input-1')
