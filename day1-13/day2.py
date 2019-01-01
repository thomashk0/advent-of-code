from collections import Counter
import sys
import itertools


def has_dup(c):
    return 2 in Counter(c).values()


def has_triple(c):
    return 3 in Counter(c).values()

def distance(w0, w1):
    return sum(cx != cy for cx, cy in zip(w0, w1))

def main():
    input = list(sys.stdin)
    dup = sum([1 if has_dup(c) else 0 for c in input])
    triple = sum([1 if has_triple(c) else 0 for c in input])
    print("Part 1: ", dup * triple)

    for p, q in itertools.product(input, input):
        if distance(p, q) == 1:
            print("Part 2:", "".join(cx for cx, cy in zip(p, q) if cx == cy))
            return

if __name__ == '__main__':
    main()
