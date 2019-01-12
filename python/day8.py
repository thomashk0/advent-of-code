import sys

def explore(l):
    n_child, n_meta = l[0], l[1]
    acc, loc = 0, 2
    for _ in range(n_child):
        w, s = explore(l[loc:])
        loc += w
        acc += s

    return loc + n_meta, acc + sum(l[loc:loc + n_meta])


def part_2(l):
    n_child, n_meta = l[0], l[1]
    loc = 2
    children = []
    for _ in range(n_child):
        w, s = part_2(l[loc:])
        children.append(s)
        loc += w

    # print(l[loc:loc+n_meta], children)
    if n_child == 0:
        return loc + n_meta, sum(l[loc:loc + n_meta])
    else:
        s = sum(children[i - 1] for i in l[loc:loc + n_meta] if (i - 1) < n_child)
        return loc + n_meta, s

                
def main():
    header = list(map(int, next(sys.stdin).split()))
    print("Part 1:", explore(header)[1])
    print("Part 2:", part_2(header)[1])


if __name__ == '__main__':
    main()
