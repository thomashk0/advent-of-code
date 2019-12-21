import intcpu
import itertools
import numpy as np


class Ascii:
    def __init__(self, src=None, cpu=None):
        self.cpu = cpu or intcpu.IntCpu()
        if src:
            self.cpu.load_file(src)
        self.non_ascii = []
        self.line = []
        self.screen = []

    def putline(self, i):
        for c in i:
            self.cpu.add_input(ord(c))
        self.cpu.add_input(ord('\n'))

    def run(self):
        should_halt = False
        while not should_halt:
            ret = self.cpu.step()
            if ret == 1:
                should_halt = True
            elif ret == 5:
                print(self.cpu.dump())
                raise Exception("No input to be provided")
            elif ret != 0:
                raise Exception("Something went wrong")

            o = self.cpu.pop_output()
            if o is None:
                continue
            if o == 10:
                if len(self.line) > 0:
                    self.screen.append(self.line)
                self.line = []
            elif 0 <= o < 128:
                self.line.append(o)
            else:
                self.non_ascii.append(o)


def draw_screen(screen):
    print("\n".join("".join(chr(c) for c in l) for l in screen))


def part_1():
    droid = Ascii('../assets/day21-input')
    # Jump as long as you need to (T <- !A or !B or !C) and you can land on
    # something (J <- T AND D)
    droid.putline("NOT A T")
    droid.putline("OR T J")
    droid.putline("NOT B T")
    droid.putline("OR T J")
    droid.putline("NOT C T")
    droid.putline("OR T J")
    droid.putline("AND D J")
    droid.putline("WALK")
    droid.run()
    print("part 1:", droid.non_ascii[0])


def part_2():
    droid = Ascii('../assets/day21-input')
    # Same as part 1, but delay the jump if you can get
    # trapped (J <- J AND (H OR E))
    droid.putline("NOT A T")
    droid.putline("OR T J")
    droid.putline("NOT B T")
    droid.putline("OR T J")
    droid.putline("NOT C T")
    droid.putline("OR T J")
    droid.putline("AND D J")
    droid.putline("NOT E T")
    droid.putline("NOT T T")
    droid.putline("OR H T")
    droid.putline("AND T J")
    droid.putline("RUN")
    droid.run()
    # draw_screen(droid.screen)
    print("part 2:", droid.non_ascii[0])


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
