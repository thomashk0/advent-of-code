from utils import parse_ints
import time

MOD = 20201227


def aoc_run(input_path):
    pk_c, pk_d = parse_ints(open(input_path).read())

    start = time.monotonic()
    k = 1
    dlog = {}
    for i in range(MOD):
        dlog[k] = i
        k = (7 * k) % MOD
    elapsed = time.monotonic() - start
    sk_c = dlog[pk_c]
    sk_d = dlog[pk_d]
    print("secret keys:", sk_c, sk_d)
    handshake_c = pow(pk_d, sk_c, MOD)
    handshake_d = pow(pk_c, sk_d, MOD)
    assert handshake_c == handshake_d
    print("part 1:", handshake_c)
    print("elapsed:", elapsed)


if __name__ == '__main__':
    aoc_run('assets/day25-input-1')
