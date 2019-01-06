import sys
import itertools


def react(s):
    i = 0
    s = s + s[-1]
    result = ""
    while i < len(s) - 1:
        if s[i] != s[i + 1] and s[i].lower() == s[i + 1].lower():
            i += 2
        else:
            result += s[i]
            i += 1
    return result


def collapse(s):
    while True:
        s_new = react(s)
        if s == s_new:
            break
        s = s_new
    return s_new


def main():
    input = next(sys.stdin).strip()
    print("Part 1:", len(collapse(input)))

    alphabet = set(input.lower())
    print("Part 2:", min([len(collapse("".join(filter(lambda x: x.lower() != c, input)))) for c in
         alphabet]))


if __name__ == '__main__':
    main()
