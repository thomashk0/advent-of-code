import itertools
import networkx as nx


class SimulationBreak(Exception):
    pass


class CpuState:
    def __init__(self):
        self.imem = []
        self.cycles = 0
        self.accumulator = 0
        self.pc = 0

    def step(self):
        self.cycles += 1
        opc, arg = self.imem[self.pc]
        if opc == 'acc':
            self.accumulator += arg
            self.pc += 1
        elif opc == 'nop':
            self.pc += 1
        elif opc == 'jmp':
            self.pc += arg
        else:
            raise ValueError(f"unsupported opcode {opc}")


def load_insn(lines):
    insn = []
    for line in lines:
        # print(line)
        opcode, arg = tuple(line.strip().split())
        arg = int(arg)
        insn.append((opcode, arg))
    return insn


def solve_part_1(insn, limit=None):
    cpu = CpuState()
    cpu.imem = insn
    explored = set()
    while True:
        if cpu.cycles == limit:
            raise SimulationBreak
        if cpu.pc in explored:
            return cpu.accumulator, cpu.cycles
        explored.add(cpu.pc)
        cpu.step()


def solve_part_2(insn, max_cycles=1000):
    pc_end = len(insn)
    for pc, (opc, arg) in enumerate(insn):
        if opc == 'jmp' or opc == 'nop':
            insn[pc] = ('jmp' if opc == 'nop' else 'nop', arg)
            cpu = CpuState()
            # print(f"{pc:4} -> {opc} {arg} {insn[pc]}")
            cpu.imem = insn
            for i in range(max_cycles):
                if cpu.pc == pc_end:
                    return cpu.accumulator, cpu.cycles
                cpu.step()
            insn[pc] = (opc, arg)
    pass


def aoc_run(filename='assets/day8-input'):
    insn = load_insn(open(filename))
    part_1 = solve_part_1(insn)
    print("part 1:", part_1[0])
    part_2 = solve_part_2(insn)
    print("part 2:", part_2[0])


if __name__ == '__main__':
    aoc_run()
