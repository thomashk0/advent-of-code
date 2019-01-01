import sys

def main():
    freqs = [int(l) for l in sys.stdin]
    print("Part 1:", sum(freqs))

    reached_once = {0}
    accum = 0
    while True:
        for f in freqs:
            accum += f
            if accum in reached_once:
                print("Part 2:", accum)
                return
            reached_once.add(accum)
    print(accum)


if __name__ == '__main__':
    main()