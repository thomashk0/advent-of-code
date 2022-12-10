from pathlib import Path


class CPU:
    def __init__(self, insn):
        self.insn = insn
        self.pc = 0
        self.cycle = 0
        self.remaining = []
        self.x = 1

    def advance(self):
        self.cycle += 1
        if self.remaining:
            cycle, new_x = self.remaining[0]
            if cycle == 0:
                self.x = new_x
                self.remaining.pop()
            else:
                self.remaining[0][0] -= 1

        if not self.remaining:
            opcode, arg = self.insn[self.pc]
            self.pc += 1
            if opcode == "noop":
                pass
            elif opcode == "addx":
                self.remaining.append([1, self.x + arg])


def parse_input(raw: str):
    cmds = []
    for line in raw.splitlines():
        ws = line.split()
        if ws[0] == "addx":
            cmds.append((ws[0], int(ws[1])))
        elif ws[0] == "noop":
            cmds.append((ws[0], []))
        else:
            assert False
    return cmds


def part_1(input):
    cpu = CPU(input)
    match = [20, 60, 100, 140, 180, 220, 10000]
    signals = []
    for i in range(240):
        cpu.advance()
        if cpu.cycle == match[0]:
            signals.append(match[0] * cpu.x)
            match = match[1:]
    return sum(signals)


def part_2(input):
    cpu = CPU(input)
    crt = [["." for _ in range(40)] for _ in range(6)]
    for i in range(6):
        for j in range(40):
            cpu.advance()
            if abs(cpu.x - j) <= 1:
                crt[i][j] = "#"
    screen = "\n".join("".join(row) for row in crt)
    print(screen)
    return screen


def aoc_inputs():
    return {
        "example": (
            "day10-input-ex",
            13140,
            Path("assets/day10-input-ex-part2").read_text(),
        ),
        "real": ("day10-input-1", 14320, None),
    }
