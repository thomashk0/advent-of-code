import itertools


def parse_questions(lines):
    all_groups = []
    group = []
    for line in itertools.chain(lines, ['\n']):
        line = line.strip()
        if not line:
            all_groups.append(group)
            group = []
            continue
        group.append(line)
    return all_groups


def all_questions(group):
    uniq = set().union(*group)
    return uniq


def awnsered(group):
    if len(group) == 1:
        return set(group[0])
    else:
        inter = set(group[0]).intersection(*group[1:])
        return inter


def main():
    questions = parse_questions(open('assets/day6-input'))
    part_1 = sum(len(all_questions(group)) for group in questions)
    print("part 1:", part_1)

    part_2 = sum(len(awnsered(group)) for group in questions)
    print("part 2:", part_2)


if __name__ == '__main__':
    main()
