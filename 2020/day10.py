def num_arragements(jolts):
    res = [0] * len(jolts)
    res[-1] = 1
    for j in reversed(range(len(jolts) - 1)):
        tot = 0
        # print(res)
        for k in range(1, 4):
            new_loc = j + k
            if new_loc >= len(jolts):
                break
            diff = jolts[new_loc] - jolts[j]
            if diff > 3:
                break
            tot += res[new_loc]
        res[j] = tot
    return res[0]


def aoc_run(filename='assets/day10-input'):
    jolts = list(map(int, open(filename)))
    built_in = max(jolts) + 3
    jolts.append(0)
    jolts.append(built_in)
    jolts.sort()
    dist = [0] * 4
    for p, n in zip(jolts, jolts[1:]):
        diff = n - p
        dist[diff] += 1
    print("part 1:", dist[1] * dist[3])
    p2 = num_arragements(jolts)
    print("part 2:", p2)


if __name__ == '__main__':
    aoc_run()
