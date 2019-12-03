
def step(state, elves):
    elf_0, elf_1 = elves
    s = state[elf_0] + state[elf_1]
    if s < 10:
        state.append(s % 10)
    else:
        state.extend([s // 10, s % 10])
    elf_0 = (elf_0 + state[elf_0] + 1) % len(state)
    elf_1 = (elf_1 + state[elf_1] + 1) % len(state)
    return elf_0, elf_1


def part_1(n):
    state = [3, 7]
    elves = (0, 1)

    while len(state) <= n + 10:
        elves = step(state, elves)
        # print(f"Step {i}")
        # print(elves, " ".join(map(str, state)))

    part_1 = ''.join(map(str, state[n:n + 10]))
    print('Part 1: {}'.format(part_1))
    return state


def part_2(n):
    puzzle_input = str(n)
    state = [3, 7]
    elves = (0, 1)
    i = -1
    while True:
        # print("part2: using n={}".format(n))
        while len(state) <= n:
            elves = step(state, elves)
        s = ''.join(map(str, state))
        i = s.find(puzzle_input)
        if i >= 0:
            break
        n *= 2
    print("Part 2: {}".format(i))


def main():
    my_input = 260321
    for n in [9, 5, 18, 2018, 260321]:
        print("== Solving for n={}".format(n))
        part_1(n)

    part_2(my_input)



if __name__ == '__main__':
    main()