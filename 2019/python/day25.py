import json

import intcpu
import itertools
import numpy as np


class NoMoreInput(Exception):
    pass


class Ascii:
    def __init__(self, src=None, cpu=None):
        self.cpu = cpu or intcpu.IntCpu()
        if src:
            self.cpu.load_file(src)
        self.non_ascii = []
        self.line = []
        self.screen = []
        self.history = []

    def clear_screen(self):
        self.screen.clear()

    def draw_screen(self):
        draw_screen(self.screen)

    def putline(self, i):
        for c in i:
            self.cpu.add_input(ord(c))
        self.cpu.add_input(ord('\n'))

    def run(self, interactive=False):
        should_halt = False
        while not should_halt:
            ret = self.cpu.step()
            if ret == 1:
                should_halt = True
            elif ret == 5:
                if interactive:
                    self.draw_screen()
                    p = input()
                    self.history.append(p)
                    self.putline(p)
                    self.clear_screen()
                    self.cpu.resume()
                else:
                    raise NoMoreInput
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
        return 0


def draw_screen(screen):
    print("\n".join("".join(chr(c) for c in l) for l in screen))


def powerset(iterable):
    """
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    xs = list(iterable)
    # note we return an iterator rather than a list
    return itertools.chain.from_iterable(
        itertools.combinations(xs, n) for n in range(1, len(xs) + 1))


def interactive():
    droid = Ascii('assets/day25-input')
    try:
        droid.run(interactive=True)
        droid.draw_screen()
    except Exception as e:
        print(droid.history)
        print(droid.draw_screen())
        droid.cpu.dump()
        print(e)
    finally:
        print(droid.non_ascii)
        json.dump(droid.history, open("history.json", "w"))


def part_1():
    droid = Ascii('assets/day25-input')
    history = json.load(open("assets/day25-replay.json"))
    for cmd in history:
        droid.putline(cmd)
    try:
        droid.run(interactive=False)
    except NoMoreInput:
        pass
    finally:
        droid.draw_screen()
    droid.clear_screen()

    items = ["wreath", "coin", "cake", "hologram", "hypercube"]
    for el in powerset(items):
        d = Ascii(cpu=droid.cpu.clone())
        for e in el:
            d.putline(f"take {e}")
        d.putline("south")
        d.cpu.resume()
        try:
            d.run(interactive=False)
            d.draw_screen()
            print("Correct item combinaison was:", el)
            return
        except NoMoreInput:
            pass


def main():
    part_1()


if __name__ == "__main__":
    main()
