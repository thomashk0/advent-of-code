import itertools


def btree_loc(directions):
    w = 2 ** (len(directions) - 1)
    l = 0
    for go_low in directions:
        if not go_low:
            l += w
        w >>= 1
    return l


def decode_passport(code):
    row_spec = code[:7]
    col_spec = code[7:]
    row_id = btree_loc([c == 'F' for c in row_spec])
    col_id = btree_loc([c == 'L' for c in col_spec])
    return row_id, col_id


def seat_id(code):
    row_id, col_id = decode_passport(code)
    return row_id * 8 + col_id


def test_decoding():
    vectors = [
        ("FBFBBFFRLR", 44, 5, 357),
        ("BFFFBBFRRR", 70, 7, 567),
        ("FFFBBBFRRR", 14, 7, 119),
        ("BBFFBBFRLL", 102, 4, 820)]
    for code, row_id, col_id, seat in vectors:
        assert decode_passport(code) == (row_id, col_id)
        assert seat_id(code) == seat


def aoc_run(filename):
    lines = list(line.strip() for line in open(filename))
    seats = set(seat_id(code) for code in lines)
    print("part 1:", max(seats))

    for c in seats:
        if c + 1 not in seats and c + 2 in seats:
            print("part 2:", c + 1)


if __name__ == '__main__':
    aoc_run('assets/day5-input')
