import intcpu
import itertools
import numpy as np


class Ascii:
    def __init__(self, src=None, cpu=None):
        self.cpu = cpu or intcpu.IntCpu()
        if src:
            self.cpu.load_file(src)
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
            else:
                self.line.append(o)


class Robot:
    def __init__(self, loc, dir):
        self.loc = loc
        self.dir = dir

    def forward(self):
        return self.loc[0] + self.dir[0], self.loc[1] + self.dir[1]

    def at_left(self):
        dx, dy = self.dir
        x, y = self.loc
        return x - dy, y + dx

    def at_right(self):
        dx, dy = self.dir
        x, y = self.loc
        return x + dy, y - dx

    def move_forward(self):
        self.loc = self.forward()

    def turn_left(self):
        self.dir = (-self.dir[1], self.dir[0])

    def turn_right(self):
        self.dir = (self.dir[1], -self.dir[0])


def draw_screen(screen):
    print("\n".join("".join(chr(c) for c in l) for l in screen))


def part_1():
    p = Ascii('../assets/day17-input')
    p.run()
    shape = [['.', '#', '.'], ['#', '#', '#'], ['.', '#', '.']]
    w = np.array([list(map(ord, l)) for l in shape], dtype=np.uint8)
    screen = np.array(p.screen, dtype=np.uint8)
    coords = []
    for i in range(screen.shape[0] - 3):
        for j in range(screen.shape[1] - 3):
            if np.all(screen[i:i + 3, j:j + 3] == w):
                coords.append((i + 1, j + 1))
    return coords, screen


def build_path(screen, loc):
    def is_dust(p):
        px, py = p
        if 0 <= px < screen.shape[0] and 0 <= py < screen.shape[1]:
            return screen[px][py] == ord('#')
        return False

    robot = Robot(loc, (-1, 0))
    path = []
    while True:
        while is_dust(robot.forward()):
            robot.move_forward()
            path.append('-')
        if is_dust(robot.at_left()):
            path.append('L')
            robot.turn_left()
            continue
        if is_dust(robot.at_right()):
            path.append('R')
            robot.turn_right()
            continue
        break
    return path


def pack(s):
    out = []
    while len(s) > 0:
        if s[0] in ['L', 'R']:
            out.append(s[0])
            s = s[1:]
        else:
            n = len(list(itertools.takewhile(lambda c: c == '-', s)))
            out.append(str(n))
            s = s[n:]
    return out


def check_patterns(path, patterns):
    ps = path
    for p, label in zip(patterns, ["A", "B", "C"]):
        ps = ps.replace(p, label)
    return not any(filter(lambda c: c == '-', ps))


def check_path(screen, loc):
    ps = "".join(build_path(screen, loc))
    patterns = [
        "L------L----------L----------L------",
        "L------L----R------------",
        "L------R------------R------------L--------"
    ]
    for p, label in zip(patterns, ["A", "B", "C"]):
        s = ",".join(pack(p))
        print(f"{label} = {s} (len={len(s)})")
        ps = ps.replace(p, label)
    print(ps)


def part_2(screen):
    x, y = tuple(np.argwhere(screen == ord('^'))[0])
    print(f"origin at ({x}, {y})")
    # return check_path(screen, (x, y))
    p = Ascii('../assets/day17-input')
    p.cpu.write(0, 2)

    patterns = [
        "L------L----------L----------L------",
        "L------L----R------------",
        "L------R------------R------------L--------"
    ]
    p.putline("B,C,B,A,C,B,A,C,B,A")
    for label, x in zip(["A", "B", "C"], patterns):
        s = ",".join(pack(x))
        p.putline(s)
        print(f"{label} = {s}")
    p.putline("n")
    p.run()
    print("part 2:", p.line[0])
    # draw_screen(p.screen)
    # print(p.screen)
    return
    # print(pack(patt[0]))
    # ps = ps.replace("L------L----R------------L------", "A")
    # ps = ps.replace("R------------R------------L--------", "B")
    # ps = ps.replace("L----------L----------L------L------", "C")
    # print(ps)
    # print(len(p))

    return

    # p.cpu.invert_branch(1146)
    p.putline('A')
    p.putline(','.join(['L'] * 11))
    p.putline('L')
    p.putline('L')
    # p.putline('R,12')
    # p.putline('L,2'*10)
    p.putline('n')
    p.run()
    # for i in range(10000):
    #     if p.cpu.read(i) == 51:
    #         print(i)
    draw_screen(p.screen)
    p.cpu.dump()
    pass


def main():
    coords, screen = part_1()
    print("part 1:", sum(x * y for x, y in coords))
    part_2(screen)


if __name__ == "__main__":
    main()
