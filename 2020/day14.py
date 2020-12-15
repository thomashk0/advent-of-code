import re
import itertools

MASK_RE = re.compile(r"mask = (\w+)$")
MEM_RE = re.compile(r"mem\[(\d+)\] = (\d+)$")


def parse(lines):
    for line in lines:
        m = MASK_RE.match(line)
        if m:
            yield 'mask', m.group(1)
            continue
        m = MEM_RE.match(line)
        if m:
            yield 'mem', (int(m.group(1)), int(m.group(2)))


def part_1(cmds):
    state = {}
    pmask = 0
    nmask = 0
    for t, args in cmds:
        if t == 'mask':
            pmask, nmask = 0, 0
            for i, c in enumerate(reversed(args)):
                if c == '0':
                    nmask |= (1 << i)
                elif c == '1':
                    pmask |= (1 << i)
            nmask = 2 ** 36 - nmask - 1
        elif t == 'mem':
            k, v = args
            state[k] = (v | pmask) & nmask
    # print(state)
    return sum(v for v in state.values())


def part_2(cmds):
    state = {}
    pmask, nmask = 0, 0
    floating_bits = []
    for t, args in cmds:
        if t == 'mask':
            pmask = 0
            floating_bits = []
            for i, c in enumerate(reversed(args)):
                if c == '1':
                    pmask |= (1 << i)
                elif c == 'X':
                    floating_bits.append(i)
        elif t == 'mem':
            k, v = args
            bits = [(0, 1)] * len(floating_bits)
            for b in itertools.product(*bits):
                addr = k | pmask
                for bit, bit_val in zip(floating_bits, b):
                    if bit_val == 0:
                        addr &= (2 ** 36 - 1) - (1 << bit)
                    else:
                        addr |= (1 << bit)
                state[addr] = v
                # print(f"Write[{addr}] -> {v}")
    return sum(v for v in state.values())


def aoc_run(input_path):
    cmd = list(parse(open(input_path)))
    p1 = part_1(cmd)
    print("part 1:", p1)
    p2 = part_2(cmd)
    print("part 2:", p2)
    pass


if __name__ == '__main__':
    aoc_run('assets/day14-input-1')
