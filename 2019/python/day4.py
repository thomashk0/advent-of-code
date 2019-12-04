def digits(x):
    while True:
        r = x % 10
        yield r
        if x < 10:
            return
        x = x // 10


def is_sorted(l):
    for i in range(len(l) - 1):
        if l[i] > l[i + 1]:
            return False
    return True


def has_doubles(l):
    n = 0
    for i in range(len(l) - 1):
        if l[i] == l[i + 1]:
            return True
    return False


def has_exact_doubles(l):
    old = l[0]
    cnt = 0
    for c in l[1:]:
        if c == old:
            cnt += 1
        else:
            if cnt == 1:
                return True
            cnt = 0
        old = c
    return cnt == 1


def is_valid_password(x, exact=False):
    ds = list(digits(x))
    ds.reverse()
    assert len(ds) <= 6
    if not is_sorted(ds):
        return False
    return has_exact_doubles(ds) if exact else has_doubles(ds)


def main():
    assert is_valid_password(111111)
    assert not is_valid_password(223450)
    assert not is_valid_password(123789)
    assert is_valid_password(123444)
    assert is_valid_password(111122, exact=True)
    assert not is_valid_password(123444, exact=True)
    assert is_valid_password(112233, exact=True)
    assert not has_exact_doubles([1, 1, 1])
    assert not has_exact_doubles([1])
    assert has_exact_doubles([1, 1])
    assert not has_exact_doubles([2, 2, 2, 2, 1])

    with open('assets/day4-input') as f:
        start, end = map(int, f.readline().split('-'))
        n = sum(map(is_valid_password, range(start, end + 1)))
        print("part 1:", n)
        n = sum(
            map(lambda x: is_valid_password(x, True), range(start, end + 1)))
        print("part 2:", n)


if __name__ == '__main__':
    main()
