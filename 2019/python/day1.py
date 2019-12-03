def fuel(mass):
    return (mass // 3) - 2


def fuel_amount(mass):
    f = fuel(mass)
    acc = 0
    while f > 0:
        acc += f
        f = fuel(f)
    return acc


def main():
    assert fuel(12) == 2
    assert fuel(14) == 2
    assert fuel(100756) == 33583
    with open('assets/day1-input') as f:
        res = sum(fuel(int(l)) for l in f)
        print(f"part 1: {res}")

    assert fuel_amount(1969) == 966
    assert fuel_amount(14) == 2
    assert fuel_amount(100756) == 50346
    with open('assets/day1-input') as f:
        res = sum(fuel_amount(int(l)) for l in f)
        print(f"part 2: {res}")


if __name__ == '__main__':
    main()
