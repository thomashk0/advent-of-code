import intcpu
import itertools
import collections



class CpuHalted(Exception):
    pass


class Droid:
    DIR_MAP = {'R': (1, 0), 'U': (0, -1), 'L': (-1, 0), 'D': (0, 1), '-': (0, 0)}

    def __init__(self, src=None, cpu=None):
        self.cpu = cpu or intcpu.IntCpu()
        if src:
            self.cpu.load_file(src)
        self.old_loc = (0, 0)
        self.loc = (0, 0)
        self.next_loc = None

    def _step(self):
        assert self.next_loc is not None
        nx, ny = self.next_loc
        cpu = self.cpu.clone()
        cpu.add_input(nx)
        cpu.add_input(ny)
        while True:
            ret = cpu.step()
            if ret == 1:
                raise CpuHalted()
            if ret == 2:
                raise Exception("No input to be provided")
            o = cpu.pop_output()
            if o is not None:
                return o

    def goto(self, dst):
        self.next_loc = dst
        o = self._step()
        self.loc = self.next_loc
        self.next_loc = None
        return o

    def move(self, d):
        dx, dy = Droid.DIR_MAP[d]
        return self.goto((self.loc[0] + dx, self.loc[1] + dy))


def draw(m, n):
    for y in range(n):
        print("".join('#' if m.get((x, y), 0) else '.' for x in range(50)))


def part_1(path, n=50, origin=(0, 0)):
    world = {}
    droid = Droid(path)
    droid.loc = origin
    world[droid.loc] = droid.move('-')
    for y, m in zip(range(n), itertools.cycle(['R', 'L'])):
        for x in range(n):
            world[droid.loc] = droid.move(m)
        if y != n - 1:
            world[droid.loc] = droid.move('D')
    # draw(world, n)
    return world, collections.Counter(world.values())[1]


def beam_shape(droid):
    x0 = droid.loc[0]
    while droid.move('R') != 1:
        pass
    x = droid.loc[0]
    w = 0
    while droid.move('R') != 0:
        w += 1
    return x, w


def can_hold_square(beam_info):
    s, _, w = beam_info[0]
    e = s + w
    for x, y, w in beam_info[:100]:
        s = max(x, s)
        e = min(e, x + w)
    return e - s + 1 >= 100, (s, e)


def part_2(path):
    droid = Droid(path)
    estimates = []
    for y in range(5, 30):
        droid.goto((0, y))
        x0, w0 = beam_shape(droid)
        estimates.append((x0 / y, w0 / y))
    x_min = min(x for x, _ in estimates)
    x_max = max(x for x, _ in estimates)
    w_min = min(w for _, w in estimates)
    y_est = int((100 * x_min  + 100) / (w_min + x_max - x_min)) - 100
    print("y estimate =", y_est)
    beam_info = []
    for y in range(y_est, y_est + 150):
        x0 = int(0.7 * y)
        assert(droid.goto((x0, y)) == 0)
        x0, w0 = beam_shape(droid)
        beam_info.append((x0, y, w0))
    for i in range(len(beam_info) - 100):
        x0, y0, w0 = beam_info[i]
        ok, (x_s, x_e) = can_hold_square(beam_info[i:])
        if ok:
            return x_s, y0
    return None
    pass

def main():
    w, r = part_1("../assets/day19-input", 50)
    print("part 1:", r)
    x, y = part_2("../assets/day19-input")
    print("part 2:", x * 10000 + y)
    # for y in range(5, 50):
    #     width = sum(w.get((x, y), 0) for x in range(50))
    #     c = min(x for x in range(50) if w.get((x, y), 0))
    #     props[y] = c, width
    #     w_interp = width / y
    #     x_interp = c / y
    #     print(f"{y:2} -> {width:3} {c} {w_interp:.3f} {x_interp:.3f}")


if __name__ == "__main__":
    main()
